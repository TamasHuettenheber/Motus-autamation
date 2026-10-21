#!/usr/bin/env python3
"""Produce one original, unpublished Jori & Flimm story draft. Never publishes."""
import argparse
import datetime as dt
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]

def read_json(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))

def normalized(s):
    return re.sub(r"[^\w]+", " ", unicodedata.normalize("NFKC", s).casefold()).strip()

def validate(d, previous, number):
    for name in ("title", "hook", "narration", "continuity_note", "next_cliffhanger"):
        if not isinstance(d.get(name), str) or len(d[name].strip()) < (300 if name == "narration" else 12):
            raise ValueError(f"Invalid story field: {name}")
    if len(d["narration"]) > 1900:
        raise ValueError("Narration too long")
    spoken=normalized(d["narration"])
    if spoken.count("jori") < 2 or spoken.count("flimm") < 2:
        raise ValueError("Jori and Flimm must BOTH remain active protagonists")
    # Main characters must be named in the clip, not merely in title metadata.

    if len(d.get("scene_briefs", [])) != 6 or any(
        not isinstance(s, str) or len(s) < 25 for s in d["scene_briefs"]
    ):
        raise ValueError("Exactly six detailed visual briefs are required")
    r = d.get("riddle")
    if not isinstance(r, dict) or any(
        not isinstance(r.get(k), str) or len(r[k]) < 3 for k in ("type", "question", "answer")
    ):
        raise ValueError("Riddle incomplete")
    pause = int(r.get("pause_seconds", 0))
    if not 5 <= pause <= 10:
        raise ValueError("Riddle pause must be 5-10 seconds")
    marker = f"[[PAUSE:{pause}]]"
    if d["narration"].count(marker) != 1:
        raise ValueError("Exactly one matching narration pause is required")
    before, after = d["narration"].split(marker)
    if normalized(r["question"]) not in normalized(before):
        raise ValueError("Riddle question must be spoken before the pause")
    if normalized(r["answer"]) not in normalized(after):
        raise ValueError("Riddle answer must follow the pause")
    for old in previous:
        if int(old.get("episode_number", -1)) == number:
            raise ValueError("Episode number already in ledger")
        for field in ("title", "hook"):
            if normalized(old.get(field, "")) == normalized(d[field]):
                raise ValueError(f"Duplicate {field}")
        if normalized((old.get("riddle") or {}).get("question", "")) == normalized(r["question"]):
            raise ValueError("Duplicate riddle")
    return True

def generate(prompt, model, temperature=0.85):
    key = os.environ.get("JORI_GEMINI_API_KEY")
    if not key:
        raise RuntimeError("Missing GitHub secret JORI_GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    request = urllib.request.Request(
        url, method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        data=json.dumps({
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": temperature,
                "maxOutputTokens": 2600
            }
        }).encode()
    )
    try:
        with urllib.request.urlopen(request, timeout=100) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Text generator HTTP {exc.code}; no draft saved") from exc
    try:
        text = "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])
        return json.loads(text)
    except (KeyError, ValueError, TypeError, IndexError) as exc:
        raise RuntimeError("Invalid generator JSON; no draft saved") from exc

def generate_and_validate(prompt, model, previous, episode_number):
    """One bounded correction attempt; never save content that fails QC."""
    candidate = generate(prompt, model)
    try:
        validate(candidate, previous, episode_number)
        return candidate
    except (ValueError, TypeError, KeyError) as first_error:
        print(f"STORY_QC_REPAIR_REQUESTED: {first_error}", flush=True)
        correction_prompt = (
            "Du bearbeitest einen bereits erzeugten, aber nicht freigegebenen "
            "deutschen Kinderstory-Entwurf. Behebe den Qualitätsfehler "
            "ohne neue Buchrätsel oder Brüche der Erzählung. "
            "Antworte NUR als vollständig gültiges JSON-Objekt mit denselben "
            "Pflichtfeldern wie der Entwurf. "
            "Die wortwörtliche Zeichenfolge von riddle.question (inklusive "
            "Satzzeichen) MUSS in narration VOR der einzigen Denkpause "
            "[[PAUSE:7]] stehen. Die wortwörtliche Zeichenfolge "
            "riddle.answer MUSS in narration DANACH stehen. "
            "Behalte genau sechs bildgeeignete scene_briefs. "
            "Korrigiere den genannten Fehler, niemals einfach QC-Gates "
            "auf true setzen.\n\n"
            f"FEHLER: {str(first_error)}\n\n"
            f"ENTWURF: {json.dumps(candidate, ensure_ascii=False)}"
        )
        corrected = generate(correction_prompt, model, temperature=0.2)
        validate(corrected, previous, episode_number)
        return corrected

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default="gemini-3.5-flash-lite")
    a = parser.parse_args()
    target = a.date or (dt.datetime.now(ZoneInfo("Europe/Berlin")).date() +
                        dt.timedelta(days=1)).isoformat()
    dt.date.fromisoformat(target)
    state = read_json("state/series-state.json")
    ledger = read_json("state/episode-ledger.json")
    folder = BASE / "drafts"
    draft_entries = [
        json.loads(p.read_text(encoding="utf-8")) for p in folder.glob("*.json")
    ] if folder.exists() else []
    # Unapproved video previews also reserve their episode number. This prevents
    # the nightly writer from replacing the already-tested episode 002.
    preview_entries = []
    for p in (BASE / "episodes").glob("*.json"):
        item = json.loads(p.read_text(encoding="utf-8"))
        if item.get("preview_only") is True and int(item.get("episode_number", -1)) >= int(state["next_episode_number"]):
            preview_entries.append(item)
    pending = sorted(
        draft_entries + preview_entries, key=lambda item: int(item["episode_number"])
    )
    numbers = [int(p["episode_number"]) for p in pending]
    if len(numbers) != len(set(numbers)):
        raise RuntimeError("Conflicting reserved episode numbers; no new draft")
    if any(p.get("date") == target for p in pending):
        print(f"ALREADY_EXISTS draft for {target}; no duplicate")
        return
    # A bounded seven-story pilot may be drafted without modifying approved continuity.
    # Publishing and full renderer QC remain disabled for every pending draft.
    if len(pending) >= 7:
        raise RuntimeError("Seven unpublished drafts pending; review required before more drafts")
    number = max(
        [int(state["next_episode_number"])] +
        [int(p["episode_number"]) + 1 for p in pending]
    )
    destination = folder / f"jori-flimm-{target}-e{number:03d}.json"
    bible = (BASE / "series-bible.md").read_text(encoding="utf-8")
    continuity = dict(state.get("continuity", {}))
    if "recently_used_visual_assets" in continuity:
        continuity["recently_used_visual_assets"] = list(
            dict.fromkeys(continuity["recently_used_visual_assets"][-24:])
        )[-12:]
    context = {
        "next_episode_number": number, "date": target,
        "continuity": continuity,
        "prior_episodes": [{
            "episode_number": e.get("episode_number"), "title": e.get("title"),
            "hook": e.get("hook"), "riddle": e.get("riddle")
        } for e in ledger.get("episodes", [])[-30:]],
        "unpublished_draft_continuity": [{
            "episode_number": e.get("episode_number"),
            "title": e.get("title"),
            "hook": e.get("hook"),
            "riddle": e.get("riddle"),
            "continuity_note": e.get("continuity_note"),
            "next_cliffhanger": e.get("next_cliffhanger")
        } for e in pending]
    }
    prompt = (
        f"Schreibe die neue eigenständige Folge {number:03d} von Jori & Flimm "
        f"als unmittelbare Fortsetzung. Deutsch, kindgerecht 7-10 Jahre, "
        f"fröhlich, logisch, keine bezahlten Buchmissionen, Buchlösungen oder Werbung. "
        f"JORI und FLIMM sind die beiden aktiven Hauptfiguren; mindestens zweimal "
        f"beide Namen im Sprechertext erwähnen. FLIMM muss selbst denken oder handeln, "
        f"nicht nur eine Nebenfigur beobachten. Neue Figuren dürfen die beiden nie "
        f"verdrängen; keine Geschichte fast ausschließlich über Igel oder Fremde. "
        f"Ein originelles, aus dem Video lösbares Rätsel. "
        f"Die Zeichenfolge riddle.question muss wortwörtlich inklusive Satzzeichen "
        f"in narration vor der EINZIGEN Markierung [[PAUSE:7]] vorkommen; "
        f"riddle.answer muss wortwörtlich danach vorkommen. Beide dürfen "
        f"keinesfalls nur sinngemäß paraphrasiert werden. "
        f"Ca. 650-950 Zeichen zusammenhängender Sprechertext. "
        f"Erzeuge NUR ein JSON-Objekt mit title, hook, narration, "
        f"riddle {{type,question,answer,pause_seconds:7}}, "
        f"scene_briefs (genau sechs ausführliche und zur Handlung passende "
        f"Bildanweisungen), continuity_note, next_cliffhanger. "
        f"Figuren und Folgen nicht vergessen. Keine Duplikate.\n\n"
        f"FIGUREN-BIBEL:\n{bible[:10000]}\n\nKONTINUITÄT:\n"
        f"{json.dumps(context, ensure_ascii=False)}"
    )
    if a.dry_run:
        print(f"DRY_RUN_OK {target} e{number:03d}; no AI call, no cost, no publication")
        return
    data = generate_and_validate(prompt, a.model, ledger.get("episodes", []) + pending, number)
    draft = {
        "schema_version": 1, "status": "draft_requires_illustration_and_qc",
        "approved_for_publish": False, "episode_number": number,
        "date": target, "generated_by": a.model,
        **{key: data[key] for key in
           ("title", "hook", "narration", "riddle", "scene_briefs",
            "continuity_note", "next_cliffhanger")}
    }
    folder.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as out:
        json.dump(draft, out, indent=2, ensure_ascii=False)
        out.write("\n")
    print(f"DRAFT_ONLY {destination}: No video and no publication triggered")

if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"STORY_DRAFT_BLOCKED: {exc}", file=sys.stderr)
        sys.exit(1)
