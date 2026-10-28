#!/usr/bin/env python3
"""Create Sulafat narration for episode 010, preserving exact scene-beat boundaries."""
import json,os,re,shutil,subprocess,sys
from pathlib import Path
root=Path.cwd()
base=root/"kids/jori-flimm/relaunch-v2"
e=json.loads((base/"episode_010_story_draft.json").read_text(encoding="utf-8"))
assert e["episode_number"]==10
assert e["voice"]=={"provider":"Gemini TTS 3.8","model":"gemini-3.8-flash-lite-tts","speaker_id":"Sulafat"}
assert e["narration"].count("[[PAUSE:7]]")==1
tokens=lambda s:re.findall(r"\w+",s.lower())
clean=lambda s:re.sub(r"\[\[(?:PAUSE:[0-9.]+|SEGMENT)\]\]"," ",s)
assert tokens(clean(e["narration_tts"]))==tokens(clean(e["narration"]))
work=root/"work";work.mkdir(exist_ok=True)
(work/"payload.json").write_text(json.dumps({"narration":e["narration_tts"],"voice":e["voice"]},ensure_ascii=False),encoding="utf-8")
subprocess.run([sys.executable,"kids/jori-flimm/relaunch-v2/scripts/generate_voice_gemini_e010.py"],check=True,timeout=900)
out=root/"work/episode_010";out.mkdir(parents=True,exist_ok=True)
shutil.copy2(work/"narration_source.wav",out/"narration_source.wav")
shutil.copy2(work/"voice-timeline.json",out/"voice-timeline.json")
t=json.loads((out/"voice-timeline.json").read_text(encoding="utf-8"))
expected=["speech","speech","speech","pause","speech","speech"]
assert [x["kind"] for x in t["items"]]==expected,t["items"]
assert abs(t["items"][3]["duration"]-7)<0.001
print("JORI_E010_SULAFAT_SEGMENTED_VOICE_READY",t["duration"])
