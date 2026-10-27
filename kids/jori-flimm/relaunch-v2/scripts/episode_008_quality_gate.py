#!/usr/bin/env python3
"""Fail-closed story and original-art checks for Jori & Flimm episode 008.
This gate does not claim or test TTS, render, MP4, or publication readiness.
"""
import hashlib
import json
import re
import struct
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
story = json.loads((BASE / "episode_008_story_draft.json").read_text(encoding="utf-8"))
prev = json.loads((BASE / "episode_007_story_draft.json").read_text(encoding="utf-8"))

assert story["episode_number"] == 8
assert story["series_version"] == "relaunch-v2"
assert story["approved_for_publish"] is False
assert story["status"] == "REVISION_PENDING_RENDER_QC"
assert story["voice"]["speaker_id"] == "Sulafat"
assert story["riddle"]["pause_seconds"] == 7
assert story["riddle"]["type"] == "visual"
assert story["answer"] == "Die Mondqualle!"
assert story["riddle"]["answer"] == story["answer"]
assert all(term in story["story"] for term in ("gläsernen Glocke", "lange durchsichtige Tentakel", "silberner Fleck", "Einen Panzer hatte es nicht"))
assert "dritter goldener Stern" in prev["cliff"]
assert "dritte goldene Stern" in story["hook"]
assert "schatten" in story["story"][:220].casefold() and "schatten" in prev["cliff"].casefold()
assert "im selben augenblick" in story["story"].casefold()
assert len(story["scene_briefs"]) >= 5
assert len(story["visuals"]) >= 5

full = " ".join(story[k] for k in ("hook", "story", "question", "after_answer", "cliffhanger"))
assert re.search(r"\bJori\b", full)
# No masculine pronouns used as Jori's subject or possessive in the narration.
assert not re.search(r"\b(?:er|ihm|sein|seinen|seinem)\b.{0,30}\bJori\b", full, re.I)
assert "Jori legte ein Ohr aufs Eis" in story["story"]

# The pause marker belongs in narration input; prose sequence must match.
assert "[[PAUSE:7]]" in story["narration"]
assert "[[PAUSE:7]]" in story["narration_tts"]
def plain(s):
    return " ".join(s.replace("[[PAUSE:7]]", "").replace("[[SEGMENT]]", "").split())
assert plain(story["narration"]) == plain(story["narration_tts"])

paths = [BASE / f"assets/episode-008-v1/scene-{i:02d}.png" for i in range(1, 7)]
hashes = set()
for p in paths:
    data = p.read_bytes()
    assert data.startswith(bytes.fromhex("89504e470d0a1a0a")), f"not PNG: {p}"
    width, height = struct.unpack(">II", data[16:24])
    assert abs(width / height - 9/16) <= 0.002, f"not 9:16: {p} {width}x{height}"
    digest = hashlib.sha256(data).hexdigest()
    assert digest not in hashes, f"duplicate image: {p}"
    hashes.add(digest)
assert len(hashes) == 6
assert len({b.strip() for b in story["scene_briefs"]}) == len(story["scene_briefs"])
assert story["release_blockers"], "Audio/release blockers must stay explicit"
print("JORI_E008_STORY_ART_QC_OK: 6 distinct 9:16 images; continuity and riddle validated")
print("JORI_E008_NOT_RENDER_READY: Sulafat audio, timed subtitles, and final MP4 still required")
