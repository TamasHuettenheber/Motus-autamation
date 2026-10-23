#!/usr/bin/env python3
"""Generate corrected female-Jori Sulafat audio; no edits to canonical story JSON."""
import argparse,json,os,subprocess,sys,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--episode",type=int,required=True,choices=[2,3,4,5,6]);a=p.parse_args()
root=Path.cwd();base=root/"kids/jori-flimm/relaunch-v2"
if a.episode==6:
    e=json.loads((base/"episode_006_story_draft.json").read_text(encoding="utf-8"))
else:
    e=next(x for x in json.loads((base/"staffel1_folgen_001_005.json").read_text(encoding="utf-8"))["episodes"] if x["episode_number"]==a.episode)
n=e["narration"]
if a.episode==2:n=n.replace("flüsterte er.","flüsterte sie.")
if a.episode==4:n=n.replace("sagte er.","sagte sie.")
if a.episode==5:n=n.replace("sagte er.","sagte sie.")
# Explicitly prohibit the known misgendering phrases in Jori's lines.
n=n.replace("Jori bot seine Hilfe an","Jori bot ihre Hilfe an")
n=n.replace("Jori wollte ihn nicht einfach irgendwo hineinstecken.","Jori wollte ihn nicht einfach irgendwo hineinstecken.")
assert n.count("[[PAUSE:7]]")==1
assert "flüsterte er" not in n and "sagte er" not in n
w=root/"work";w.mkdir(exist_ok=True)
(w/"payload.json").write_text(json.dumps({"narration":n,"voice":{"provider":"Gemini TTS 3.8","model":os.environ.get("JORI_TTS_MODEL","gemini-3.8-flash-lite-tts"),"speaker_id":"Sulafat"}},ensure_ascii=False))
subprocess.run([sys.executable,"kids/jori-flimm/scripts/generate_voice_gemini.py"],check=True,timeout=450)
out=root/f"work/episode_{a.episode:03d}";out.mkdir(parents=True,exist_ok=True)
shutil.copy2(w/"narration_source.wav",out/"narration_source.wav")
shutil.copy2(w/"voice-timeline.json",out/"voice-timeline.json")
t=json.loads((out/"voice-timeline.json").read_text())
assert t["items"][1]["kind"]=="pause" and abs(t["items"][1]["duration"]-7)<.12
print("JORI_CORRECTED_SULAFAT_VOICE_READY",a.episode,t["duration"])
