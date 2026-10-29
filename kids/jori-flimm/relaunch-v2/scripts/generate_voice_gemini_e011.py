#!/usr/bin/env python3
"""Generate a Jori & Flimm local waveform using Gemini 3.8's Free-Tier TTS.

Voice remains configurable; only explicitly allow mature/warm female auditions.
Narration transmitted to Google is PUBLICATION-READY STORY TEXT ONLY.
No production/publication state changes. Any API error stops rendering.
"""
import base64
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

WORK=Path("work")
MARKER=re.compile(r"\[\[PAUSE:([0-9]+(?:\.[0-9]+)?)\]\]|\[\[SEGMENT\]\]")
ALLOW={"Gacrux","Vindemiatrix","Sulafat"}
MODEL=os.environ.get("JORI_TTS_MODEL","gemini-3.8-flash-lite-tts")
STYLE=(
    "Deutsch (Deutschland); warmes natürliches Geschichtenerzählen wie eine "
    "liebevolle Großmutter, nicht lehrerhaft, nicht blechern, nicht mechanisch, "
    "nicht österreichisch, deutlich und lebendig mit freundlichem Schmunzeln. "
    "Am Vorlesesessel im Wohnzimmer, gut hörbar, nicht flüstern."
)

def tts_segment(text,voice,secret):
    payload={
        "model":MODEL,
        "input":[{"type":"user_input","content":[{
            "type":"text","text":text,
            "annotations":[{"type":"speech_metadata","style":STYLE}]
        }]}],
        "response_format":{"type":"audio"},
        "generation_config":{"speech_config":[{"voice":voice}]}
    }
    req=urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/interactions",
        method="POST",data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type":"application/json","x-goog-api-key":secret,
                 "User-Agent":"Jori-Flimm-StoryNarrator/1.0"}
    )
    try:
        with urllib.request.urlopen(req,timeout=130) as response:
            result=json.load(response)
    except urllib.error.HTTPError as e:
        # Google uses HTTP 429 for several distinct quota/rate-limit conditions.
        # Preserve only structured error fields; never log request headers or API keys.
        try:
            response=json.loads(e.read().decode("utf-8",errors="replace"))
            api_error=response.get("error",{}) if isinstance(response,dict) else {}
            diagnostic={
                "status":api_error.get("status"),
                "message":api_error.get("message"),
                "details":api_error.get("details"),
            }
            diagnostic={k:v for k,v in diagnostic.items() if v is not None}
            detail=json.dumps(diagnostic,ensure_ascii=False)[:1800]
        except Exception:
            detail=""
        suffix=f": {detail}" if detail else ""
        raise RuntimeError(f"Gemini TTS failed HTTP {e.code}{suffix}") from e
    audio=[part["data"] for step in result.get("steps",[])
           for part in step.get("content",[])
           if part.get("type")=="audio" and part.get("data")]
    if not audio:
        raise RuntimeError("Gemini TTS returned no audio; cannot render")
    raw=base64.b64decode(audio[-1],validate=True)
    if len(raw)<5000 or len(raw)>30_000_000 or raw[:4]!=b"RIFF":
        raise RuntimeError("Gemini TTS did not return a valid WAV")
    return raw

def main():
    secret=os.environ.get("JORI_GEMINI_API_KEY")
    if not secret:
        raise RuntimeError("No JORI_GEMINI_API_KEY, no paid fallback")
    p=json.loads((WORK/"payload.json").read_text(encoding="utf-8"))
    cfg=p.get("voice") or {}
    voice=cfg.get("speaker_id")
    if cfg.get("provider")!="Gemini TTS 3.8" or cfg.get("model")!=MODEL or voice not in ALLOW:
        raise ValueError("Voice provider/model/speaker_id not auditioned")
    narration=p["narration"]
    sequence=[]
    cursor=0
    for marker in MARKER.finditer(narration):
        left=narration[cursor:marker.start()].strip()
        if left:sequence.append(("speech",left))
        if marker.group(1) is not None:
            pause=float(marker.group(1))
            if pause<5 or pause>10:
                raise ValueError("Riddle pause must be 5-10 seconds")
            sequence.append(("pause",pause))
        cursor=marker.end()
    rest=narration[cursor:].strip()
    if rest: sequence.append(("speech",rest))
    if len([x for x in sequence if x[0]=="pause"]) != 1:
        raise ValueError("One explicit riddle pause required")
    d=WORK/"tts-chunks"
    d.mkdir(parents=True,exist_ok=True)
    timeline=[]
    concat=d/"concat.txt"
    cumulative=0.0
    tts_calls=0
    with concat.open("w",encoding="utf-8") as f:
        for i,(kind,value) in enumerate(sequence,1):
            dest=d/f"{i:02d}.wav"
            if kind=="speech":
                if len(value)>2500:raise ValueError("Narration chunk too long")
                source=d/f"{i:02d}-original.wav"
                if tts_calls:
                    # Stay below the verified Google Free Tier limit of 3 requests/minute.
                    time.sleep(22)
                source.write_bytes(tts_segment(value,voice,secret))
                tts_calls += 1
                subprocess.run(["ffmpeg","-nostdin","-y","-v","error","-i",str(source),
                    "-ar","24000","-ac","1","-c:a","pcm_s16le",str(dest)],
                    check=True,timeout=50)
                spoken=value
            else:
                subprocess.run(["ffmpeg","-nostdin","-y","-v","error","-f","lavfi",
                    "-i","anullsrc=r=24000:cl=mono","-t",str(value),
                    "-c:a","pcm_s16le",str(dest)],check=True,timeout=35)
                spoken=""
            with wave.open(str(dest),"rb") as w:
                dur=w.getnframes()/w.getframerate()
            if dur<0.2:raise ValueError("Empty audio segment")
            abspath=str(dest.resolve()).replace("'","'\\''")
            f.write("file '"+abspath+"'\n")
            start=cumulative
            cumulative+=dur
            timeline.append({"kind":kind,"text":spoken,"start":round(start,3),
                "end":round(cumulative,3),"duration":round(dur,3)})
    subprocess.run(["ffmpeg","-nostdin","-y","-v","error","-f","concat","-safe","0",
        "-i",str(concat),"-c","copy",str(WORK/"narration_source.wav")],
        check=True,timeout=50)
    (WORK/"voice-timeline.json").write_text(json.dumps({"items":timeline,
        "duration":round(cumulative,3),"provider":"Gemini TTS 3.8",
        "speaker_id":voice},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"GEMINI_OMI_VOICE_RENDERED {voice} seconds={cumulative:.1f}; "
          f"requests={tts_calls} spacing_seconds=22; preview pipeline only")

if __name__=="__main__":
    try:main()
    except Exception as exc:
        print(f"GEMINI_OMI_TTS_FAILURE: {exc}",file=sys.stderr)
        sys.exit(1)
