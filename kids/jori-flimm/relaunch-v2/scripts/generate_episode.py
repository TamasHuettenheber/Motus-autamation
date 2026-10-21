#!/usr/bin/env python3
"""Draft original Jori & Flimm episodes for the reboot, starting at 001.

Uses a separate new-series ledger. All drafts are NOT approved for publication.
Only user-approved real-world publishing setup may enable future delivery.
"""
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

BASE=Path(__file__).resolve().parents[1]
CANON=BASE.parent
MARKER="[[PAUSE:7]]"
FIELDS=["hook","story","after_answer","cliffhanger","scene_briefs","riddle"]

def norm(s):
    return re.sub(r"[^\w]+"," ",unicodedata.normalize("NFKC",s).casefold()).strip()

def validate_candidate(p, history, number):
    if not isinstance(p,dict):
        raise ValueError("Output must be a JSON object")
    for k in ("title","hook","story","after_answer","cliffhanger"):
        if not isinstance(p.get(k),str) or not p[k].strip():
            raise ValueError(f"Missing story section {k}")
    limits={
        "title":(8,100),"hook":(30,150),"story":(185,820),
        "after_answer":(60,330),"cliffhanger":(35,200)
    }
    for k,(low,high) in limits.items():
        if not low <= len(p[k].strip()) <= high:
            raise ValueError(f"{k} length must be {low}-{high}")
    if re.match(r"^\s*(willkommen|hallo|guten tag|heute erzählen wir|in der heutigen folge)",
                p["hook"].casefold()):
        raise ValueError("Start must immediately create tension, not a greeting")
    if not any(x in norm(p["hook"]) for x in ("plötzlich","seltsam","geheimnis",
           "verschwand","warum","wer","was","auf einmal","ein licht","knacken",
           "klingeln","flackert","funk","leucht","spurlos","zitter","flüster",
           "klopf","fremd","sonderbar")):
        raise ValueError("Hook has no concrete mystery cue")
    full=" ".join(p[k] for k in ("hook","story","after_answer","cliffhanger"))
    if len(re.findall(r"\bjori\b",full,re.I))<1 or len(re.findall(r"\bflimm\b",full,re.I))<1:
        raise ValueError("Both named lead characters must appear in narrated story")
    if any(x in norm(full) for x in ("amazon","schrittivo","motus","tiktok","like und abonnier","kaufe das buch")):
        raise ValueError("No direct marketing within children's free story")
    q=p.get("riddle")
    if not isinstance(q,dict):
        raise ValueError("Missing core riddle")
    if q.get("type") not in ("logic","pattern","counting","word","visual","direction","code"):
        raise ValueError("Unsupported riddle type")
    for key,minlen,maxlen in (("question",25,180),("answer",2,110),("evidence_in_story",15,200)):
        if not isinstance(q.get(key),str) or not minlen <= len(q[key]) <= maxlen:
            raise ValueError(f"Missing or invalid riddle {key}")
    if q.get("pause_seconds") != 7:
        raise ValueError("Riddle must contain exactly seven seconds of thinking time")
    if norm(q["evidence_in_story"]) not in norm(p["story"]):
        raise ValueError("Clue not literally present in the story before the riddle")
    if norm(q["answer"]) in norm(p["hook"]+" "+p["story"]):
        # Only reject multiword / unambiguous answers, avoid incidental common-word false positives
        if len(norm(q["answer"]))>=13:
            raise ValueError("Riddle answer spoiled before the pause")
    if not (isinstance(p.get("scene_briefs"),list) and len(p["scene_briefs"])==6):
        raise ValueError("Exactly six precise scene briefs required")
    if any(not isinstance(t,str) or len(t)<70 or len(t)>520 for t in p["scene_briefs"]):
        raise ValueError("Scene briefs must be explicit and illustrative")
    if not isinstance(p.get("critical_visual_objects"),list) or len(p["critical_visual_objects"])<1:
        raise ValueError("No critical visual objects to verify against rendered images")
    if any(not isinstance(x,str) or len(x)<4 for x in p["critical_visual_objects"]):
        raise ValueError("Invalid critical visual object")
    # The visual riddle must be introduced and depictable BEFORE the spoken question.
    scene_text=norm(" ".join(p["scene_briefs"][0:5]))
    if not any(norm(ob) in scene_text for ob in p["critical_visual_objects"]):
        raise ValueError("No critical clue explicitly requested before pause in scene briefs")
    if not norm(p["cliffhanger"]) or norm(p["cliffhanger"]) in norm(p["hook"]):
        raise ValueError("Cliffhanger cannot merely repeat the hook")
    if len(norm(p["cliffhanger"]).split())<6:
        raise ValueError("Cliffhanger must introduce a tangible new unresolved event")
    for old in history:
        if int(old.get("episode_number",-1))==number:
            raise ValueError("Episode number already reserved")
        for f in ("title","hook","cliffhanger"):
            if norm(old.get(f,""))==norm(p[f]):
                raise ValueError(f"Duplicate {f}")
        if norm((old.get("riddle") or {}).get("question",""))==norm(q["question"]):
            raise ValueError("Riddle reused")
    return True

def assemble_narration(p):
    return " ".join([
        p["hook"].strip(),p["story"].strip(),
        p["riddle"]["question"].strip(),MARKER,
        p["riddle"]["answer"].strip(),p["after_answer"].strip(),
        p["cliffhanger"].strip()
    ])

def generate(prompt,model):
    secret=os.environ.get("JORI_GEMINI_API_KEY")
    if not secret:
        raise RuntimeError("Missing JORI_GEMINI_API_KEY; no paid fallback")
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    request=urllib.request.Request(url,method="POST",data=json.dumps({
        "contents":[{"parts":[{"text":prompt}]}],
        "generationConfig":{
            "responseMimeType":"application/json","temperature":0.8,
            "maxOutputTokens":3400
        }
    },ensure_ascii=False).encode("utf-8"),headers={
        "Content-Type":"application/json","x-goog-api-key":secret
    })
    try:
        with urllib.request.urlopen(request,timeout=110) as response:
            result=json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Gemini story request rejected HTTP {exc.code}") from exc
    try:
        chunks=result["candidates"][0]["content"]["parts"]
        return json.loads("".join(x.get("text","") for x in chunks))
    except (KeyError,ValueError,IndexError,TypeError) as exc:
        raise RuntimeError("No valid generator JSON") from exc

def generate_with_one_repair(prompt,model,history,number):
    p=generate(prompt,model)
    try:
        validate_candidate(p,history,number)
        return p
    except (ValueError,KeyError,TypeError) as exc:
        print(f"REBOOT_STORY_QC_REPAIR: {exc}",flush=True)
        p2=generate(prompt + "\n\nÜberarbeite den nachfolgenden Entwurf vollständig "
             "und korrigiere folgenden Fehler, ohne Inhalte des Buches zu verraten. "
             "Behalte alle verlangten JSON-Felder. Nicht veröffentlichen. "
             f"FEHLER: {exc}\nENTWURF: {json.dumps(p,ensure_ascii=False)}",
             model)
        validate_candidate(p2,history,number)
        return p2

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--date",default="")
    parser.add_argument("--model",default="gemini-3.5-flash-lite")
    parser.add_argument("--dry-run",action="store_true")
    args=parser.parse_args()
    target=args.date or (dt.datetime.now(ZoneInfo("Europe/Berlin")).date()+
                         dt.timedelta(days=1)).isoformat()
    dt.date.fromisoformat(target)
    st=json.loads((BASE/"state/series-state.json").read_text(encoding="utf-8"))
    ledger=json.loads((BASE/"state/episode-ledger.json").read_text(encoding="utf-8"))
    if st.get("series_version")!="relaunch-v2" or ledger.get("series_version")!="relaunch-v2":
        raise RuntimeError("Wrong series; refusing to mix old episodes")
    if st.get("release_authorized") or st.get("public_tiktok_connected"):
        raise RuntimeError("Draft-only script must not control publication")
    folder=BASE/"drafts"
    pending=sorted((json.loads(x.read_text(encoding="utf-8"))
                   for x in folder.glob("*.json")),key=lambda d:int(d["episode_number"])) if folder.exists() else []
    if any(d.get("date")==target for d in pending):
        print(f"ALREADY_EXISTS_REBOOT_DRAFT {target}")
        return
    if len(pending)>=7:
        raise RuntimeError("Seven drafts without final visual/audio QC: stop")
    history=ledger.get("episodes",[])+pending
    numbers=[int(x["episode_number"]) for x in history]
    if len(numbers)!=len(set(numbers)):
        raise RuntimeError("Duplicate episode reservations")
    number=max([int(st["next_episode_number"])]+[x+1 for x in numbers])
    if number<1:raise RuntimeError("Episodes start at 001")
    dest=folder/f"jori-flimm-restart-{target}-e{number:03d}.json"
    previous=[{"episode_number":x.get("episode_number"),
               "title":x.get("title"),"cliffhanger":x.get("cliffhanger"),
               "riddle":x.get("riddle"),"continuity_note":x.get("continuity_note")}
              for x in history[-7:]]
    prompt=(
        f"Erstelle Folge {number:03d} der NEUEN Staffel Jori & Flimm. "
        "Hauptfiguren Jori und Flimm (beide aktiv), keine Werbung. "
        "WICHTIG: Die Handlung muss mindestens drei konkrete Ereignisse enthalten. "
        "Gesamtstruktur GENAU: HOOK als starker, ungewöhnlicher Einstieg "
        "in den ersten 2–4 Sekunden; STORY mit spannender kindgerechter Handlung "
        "und VOLLSTÄNDIGEN Rätselhinweisen; EINE klare Rätselfrage, danach "
        "7 Sekunden echte Denkpause (wird technisch eingesetzt); "
        "korrekte Lösung plus überraschende STORY-WENDUNG, dann ein NEUER "
        "unaufgelöster CLIFFHANGER, damit Kinder Folge 2 unbedingt sehen wollen. "
        "Kein langes Hallo, keine langweilige Lehrerstimme, keine Wiederholungen. "
        "Geschichte gemütlich-magisch, etwas witzig. "
        "Im Feld hook 30–150 Zeichen mit ungewöhnlichem Ereignis, "
        "story 270–820 Zeichen, after_answer 60–330 Zeichen, "
        "cliffhanger 35–200 Zeichen. "
        "Antworte ausschließlich mit einem JSON-OBJEKT mit Feldern: "
        "title, hook, story, after_answer, cliffhanger, "
        "riddle:{type,question,answer,pause_seconds:7,evidence_in_story}, "
        "scene_briefs:[genau sechs ausführliche und motivgetreue Anweisungen "
        "je 70–400 Zeichen],critical_visual_objects:[mindestens ein präzise "
        "benannter RÄTSELRELEVANTER sichtbarer Gegenstand/Symbol]. "
        "Die Szene VOR der Rätselantwort muss die Hinweise für Kinder "
        "tatsächlich sichtbar darstellen, zum Beispiel wenn drei Glocken "
        "mit Mond/Stern/Schneeflocke erwähnt sind müssen ALLE DREI Zeichen "
        "gut sichtbar im Bildmotiv beschrieben werden. Bildunterschriften "
        "dürfen fehlende Bildobjekte nicht ersetzen. "
        "Das Feld riddle.evidence_in_story MUSS ein wörtliches Zitat der "
        "entscheidenden Rätselhinweise aus dem Feld story sein. "
        "In Folge 001 begegnen sich Jori und Flimm erstmalig und lernen "
        "einander in einem eigenen einfachen Lichtabenteuer kennen; "
        "keine Erinnerung an die alten Testfolgen oder das Buch."
        "\nFIGUREN-BIBEL:\n"+(CANON/"series-bible.md").read_text(encoding="utf-8")[:8500]+
        "\nNEUSTART-REGELWERK:\n"+(BASE/"REGELWERK.md").read_text(encoding="utf-8")[:7000]+
        "\nKONTINUITÄT DER NEUEN STAFFEL:\n"+
        json.dumps({"series_state":st["continuity"],"previous_new_season_episodes":previous},ensure_ascii=False)
    )
    if args.dry_run:
        print(f"REBOOT_DRY_RUN_OK e{number:03d} {target}: no API call, no publication")
        return
    data=generate_with_one_repair(prompt,args.model,history,number)
    payload={
        "schema_version":2,"series_version":"relaunch-v2",
        "status":"STORY_DRAFT_NOT_READY","approved_for_publish":False,
        "episode_number":number,"date":target,"generated_by":args.model,
        "voice":{"provider":"Gemini TTS 3.8","model":"gemini-3.8-flash-tts",
                 "speaker_id":"Sulafat"},
        "narration":assemble_narration(data),
        **data,
        "qc":{"story_structure":True,"audio_transcript":False,
              "subtitle_alignment":False,"visual_story_alignment":False,
              "visible_riddle_clues":False,"final_audio":False,
              "video_integrity":False,"human_review":False},
        "tiktok_publication":False
    }
    folder.mkdir(parents=True,exist_ok=True)
    with dest.open("x",encoding="utf-8") as file:
        json.dump(payload,file,indent=2,ensure_ascii=False)
        file.write("\n")
    print(f"REBOOT_STORY_DRAFT_ONLY e{number:03d}: {dest}; no render/release")

if __name__=="__main__":
    try:main()
    except (ValueError,TypeError,KeyError,RuntimeError,OSError) as exc:
        print(f"REBOOT_DRAFT_BLOCKED: {exc}",file=sys.stderr)
        sys.exit(1)
