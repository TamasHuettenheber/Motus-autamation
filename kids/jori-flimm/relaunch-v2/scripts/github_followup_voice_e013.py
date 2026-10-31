#!/usr/bin/env python3
"""Create or reuse Sulafat narration for episode 013, preserving scene-beat boundaries."""
import hashlib,json,re,shutil,subprocess,sys,wave
from pathlib import Path
root=Path.cwd()
base=root/"kids/jori-flimm/relaunch-v2"
e=json.loads((base/"episode_013_story_draft.json").read_text(encoding="utf-8"))
assert e["episode_number"]==13
assert e["voice"]=={"provider":"Gemini TTS 3.8","model":"gemini-3.8-flash-lite-tts","speaker_id":"Sulafat"}
assert e["narration"].count("[[PAUSE:7]]")==1
tokens=lambda s:re.findall(r"\w+",s.lower())
clean=lambda s:re.sub(r"\[\[(?:PAUSE:[0-9.]+|SEGMENT)\]\]"," ",s)
assert tokens(clean(e["narration_tts"]))==tokens(clean(e["narration"]))
root_work=root/"work"
out=root_work/"episode_013"
out.mkdir(parents=True,exist_ok=True)
cache=base/"audio-cache/episode-013"
cache_audio=cache/"narration_source.wav"
cache_timeline=cache/"voice-timeline.json"
cache_manifest=cache/"voice-cache-manifest.json"
expected_manifest={"narration_sha256":hashlib.sha256(e["narration_tts"].encode("utf-8")).hexdigest(),"voice":e["voice"]}
audio=out/"narration_source.wav"
timeline=out/"voice-timeline.json"
if cache_audio.exists()!=cache_timeline.exists():
    raise RuntimeError("Incomplete cached Sulafat audio pair; refusing a fresh TTS request")
if cache_audio.exists():
    if not cache_manifest.is_file() or json.loads(cache_manifest.read_text(encoding="utf-8"))!=expected_manifest:
        raise RuntimeError("Cached Sulafat narration does not match the current approved text/voice; refusing a new TTS request")
    shutil.copy2(cache_audio,audio)
    shutil.copy2(cache_timeline,timeline)
    print("JORI_E013_SULAFAT_CACHE_REUSED; no TTS request")
else:
    root_work.mkdir(exist_ok=True)
    (root_work/"payload.json").write_text(json.dumps({"narration":e["narration_tts"],"voice":e["voice"]},ensure_ascii=False),encoding="utf-8")
    subprocess.run([sys.executable,"kids/jori-flimm/relaunch-v2/scripts/generate_voice_gemini_e013.py"],check=True,timeout=900)
    shutil.copy2(root_work/"narration_source.wav",audio)
    shutil.copy2(root_work/"voice-timeline.json",timeline)
    cache.mkdir(parents=True,exist_ok=True)
    shutil.copy2(audio,cache_audio)
    shutil.copy2(timeline,cache_timeline)
    cache_manifest.write_text(json.dumps(expected_manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("JORI_E013_SULAFAT_CACHE_CREATED")
t=json.loads(timeline.read_text(encoding="utf-8"))
expected=["speech","speech","speech","speech","pause","speech","speech"]
assert [x["kind"] for x in t["items"]]==expected,t["items"]
assert abs(t["items"][4]["duration"]-7)<0.001
with wave.open(str(audio),"rb") as w:
    assert (w.getframerate(),w.getsampwidth(),w.getnchannels())==(24000,2,1)
    pause=t["items"][4]
    w.setpos(round(pause["start"]*w.getframerate()))
    silent=w.readframes(round(7*w.getframerate()))
    assert len(silent)==7*24000*2 and not any(silent),"cached/source audio is not exactly seven seconds of silence"
print("JORI_E013_SULAFAT_SEGMENTED_VOICE_READY",t["duration"])
