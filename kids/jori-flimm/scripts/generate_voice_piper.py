#!/usr/bin/env python3
"""Offline Standard-German Piper female voice with reproducible narration timeline.

Downloaded voice: de_DE-kerstin-low (Piper German voice, CC0). Narration
stays on the GitHub runner; no public TTS demo receives the story text.
"""
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

BASE=Path("work")
MARKER=re.compile(r"\[\[PAUSE:([0-9]+(?:\.[0-9]+)?)\]\]")
VOICE="de_DE-kerstin-low"
MODEL=BASE/"voices"/f"{VOICE}.onnx"

def split_segments(text):
    result=[]
    cursor=0
    for m in MARKER.finditer(text):
        speech=text[cursor:m.start()].strip()
        if speech:result.append({"kind":"speech","text":speech})
        dur=float(m.group(1))
        if not 5 <= dur <= 10:
            raise ValueError("Riddle thinking pause outside 5-10 s")
        result.append({"kind":"pause","duration":dur})
        cursor=m.end()
    tail=text[cursor:].strip()
    if tail:result.append({"kind":"speech","text":tail})
    if not result or any("[[PAUSE:" in v.get("text","") for v in result):
        raise ValueError("Malformed pause marker")
    return result

def render():
    p=json.loads((BASE/"payload.json").read_text(encoding="utf-8"))
    config=p.get("voice") or {}
    if config.get("provider")!="Piper local TTS" or config.get("model")!=VOICE or config.get("speaker_id")!="kerstin":
        raise ValueError("German Piper voice configuration mismatch")
    if not (MODEL.is_file() and (MODEL.parent / f"{VOICE}.onnx.json").is_file()):
        raise FileNotFoundError("German Piper model not downloaded")
    blocks=split_segments(p["narration"])
    chunks=BASE/"tts-chunks"
    chunks.mkdir(parents=True,exist_ok=True)
    segments=[]
    for n,item in enumerate(blocks,1):
        out=chunks/f"{n:02d}.wav"
        if item["kind"]=="speech":
            subprocess.run([sys.executable,"-m","piper","-m",str(MODEL),
                            "--output_file",str(out),"--",item["text"]],
                           check=True,timeout=180)
        else:
            subprocess.run(["ffmpeg","-nostdin","-y","-v","error","-f","lavfi","-i",
                "anullsrc=r=24000:cl=mono","-t",str(item["duration"]),
                "-c:a","pcm_s16le",str(out)],check=True,timeout=30)
        with wave.open(str(out),"rb") as w:
            dur=w.getnframes()/w.getframerate()
        if dur<0.1:
            raise ValueError(f"Empty generated audio chunk {n}")
        segments.append({**item,"file":str(out.resolve()),"duration":dur})

    # Normalize sample rate, sample format before lossless joining.
    norm_files=[]
    for n,item in enumerate(segments,1):
        dst=chunks/f"{n:02d}-norm.wav"
        subprocess.run(["ffmpeg","-nostdin","-y","-v","error","-i",item["file"],
            "-ar","24000","-ac","1","-c:a","pcm_s16le",str(dst)],
            check=True,timeout=30)
        with wave.open(str(dst),"rb") as w:
            item["duration"]=w.getnframes()/w.getframerate()
        norm_files.append(dst.resolve())

    cursor=0.0
    timeline=[]
    concat=chunks/"concat.txt"
    with concat.open("w",encoding="utf-8") as f:
        for item,dst in zip(segments,norm_files):
            escaped=str(dst).replace("'","'\\''")
            f.write("file '"+escaped+"'\n")
            start=cursor
            cursor+=float(item["duration"])
            timeline.append({"kind":item["kind"],"text":item.get("text",""),
                "start":round(start,3),"end":round(cursor,3),
                "duration":round(float(item["duration"]),3)})
    subprocess.run(["ffmpeg","-nostdin","-y","-v","error","-f","concat","-safe","0",
        "-i",str(concat),"-c","copy",str(BASE/"narration_source.wav")],
        check=True,timeout=45)
    (BASE/"voice-timeline.json").write_text(json.dumps(
        {"items":timeline,"duration":round(cursor,3),"provider":"Piper local TTS",
         "voice":VOICE},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"PIPER_DE_VOICE_OK chunks={len(segments)} seconds={cursor:.1f} no Austrian Victoria",flush=True)

if __name__=="__main__":
    try:render()
    except Exception as exc:
        print(f"PIPER_DE_VOICE_FAILED: {exc}",file=sys.stderr)
        sys.exit(1)
