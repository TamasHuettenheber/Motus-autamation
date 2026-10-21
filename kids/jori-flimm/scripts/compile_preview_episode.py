#!/usr/bin/env python3
"""Compile an UNAPPROVED story+montage preview to a renderer test payload.

The result may trigger a video-preview Actions run, but it must NEVER approve,
schedule or publish to a social account, nor write canonical series state.
"""
import argparse
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BRANCH = "feature/jori-flimm-kids-pipeline"
RAW_ROOT = ("https://raw.githubusercontent.com/"
            "TamasHuettenheber/Motus-autamation/" + BRANCH +
            "/kids/jori-flimm/previews/")


def compile_preview(draft_path, preview_folder):
    story = json.loads(Path(draft_path).read_text(encoding="utf-8"))
    manifest = json.loads((Path(preview_folder) / "preview-manifest.json").read_text(encoding="utf-8"))
    if story.get("approved_for_publish") is not False:
        raise ValueError("Draft must be unapproved")
    if story.get("status") != "draft_requires_illustration_and_qc":
        raise ValueError("Draft is not in preview state")
    if manifest.get("status") != "PREVIEW_ONLY":
        raise ValueError("Preview artwork must explicitly be PREVIEW_ONLY")
    for field in ("episode_number", "date", "title"):
        if manifest.get(field) != story.get(field):
            raise ValueError(f"Artwork/story mismatch: {field}")
    for flag in ("approved_for_publish", "new_unique_scene_illustrations",
                 "story_specific_visuals_verified"):
        if manifest.get(flag) is not False:
            raise ValueError(f"Preview manifest must not claim {flag}")
    scenes = manifest.get("scenes", [])
    if len(scenes) != 6 or len({p.get("file") for p in scenes}) != 6:
        raise ValueError("Need six unique scene files")
    episode = int(story["episode_number"])
    basename = f"{story['date']}-e{episode:03d}"
    if Path(preview_folder).name != basename:
        raise ValueError("Artwork directory name does not match episode")
    out_scenes=[]
    for i, scene in enumerate(scenes, 1):
        if scene.get("order") != i or scene.get("art_alignment_confirmed") is not False:
            raise ValueError("No scene can claim verified new story illustrations")
        name = scene.get("file")
        if not isinstance(name, str) or not re.fullmatch(r"scene-\d\d\.jpg", name):
            raise ValueError("Unexpected scene file")
        if not (Path(preview_folder) / name).is_file():
            raise ValueError("Required scene image missing")
        out_scenes.append({
            "order": i, "duration_seconds": 11,
            "image_url": RAW_ROOT + basename + "/" + name,
            "caption": story["scene_briefs"][i-1][:140]
        })
    riddle = story.get("riddle", {})
    if riddle.get("type") not in {"pattern","counting","logic","direction","word","visual","code"}:
        raise ValueError("Unknown riddle type; human check required")
    return {
        "date": story["date"],
        "episode_number": episode,
        "title": story["title"],
        "hook": story["hook"],
        "narration": story["narration"],
        "riddle": riddle,
        "scenes": out_scenes,
        "voice": {
            "provider": "Gemini TTS 3.8",
            "model": "gemini-3.8-flash-tts",
            "speaker_id": "Sulafat",
            "speed": 1.0
        },
        "publish_time": "14:00",
        "qc": {
            "book_spoiler_check": False,
            "continuity_check": False,
            "duplicate_check": False
        },
        "preview_only": True,
        "continuity_note": story["continuity_note"],
        "cta": "Fortsetzung morgen auf Jori & Flimm."
    }


def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("--draft", required=True, type=Path)
    arg.add_argument("--preview-folder", required=True, type=Path)
    arg.add_argument("--output-dir", default=BASE / "episodes", type=Path)
    args=arg.parse_args()
    payload=compile_preview(args.draft,args.preview_folder)
    out=args.output_dir / (
        f"jori-flimm-{payload['date']}-e{payload['episode_number']:03d}.json"
    )
    if out.exists():
        raise FileExistsError(f"Preview episode already exists: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x",encoding="utf-8") as f:
        json.dump(payload,f,ensure_ascii=False,indent=2)
        f.write("\n")
    print(f"CREATED_UNAPPROVED_VIDEO_PREVIEW {out}; no public publishing")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as exc:
        print(f"COMPILE_PREVIEW_BLOCKED: {exc}",file=sys.stderr)
        sys.exit(1)
