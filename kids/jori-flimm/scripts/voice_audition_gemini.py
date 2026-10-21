#!/usr/bin/env python3
"""Generate three *unpublished* mobile-loudness German story voice auditions.

A real owned Gemini API key is supplied by GitHub Actions Secrets only.
No key is printed or stored. Free-tier use only; one short request per voice.
The chosen voice is NOT automatically applied to production.
"""
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODEL="gemini-3.8-flash-tts"
VOICES=["Gacrux","Vindemiatrix","Sulafat"]
TRANSCRIPT=(
    "Kaum hatten Jori und Flimm das alte Brückentor geöffnet, hörten sie ein "
    "leises Klingeln. Flimm schaute Jori mit großen Augen an. "
    "Sein kleiner Sternenbauch begann golden zu leuchten. "
    "Du meine Güte, was war denn hier passiert? "
    "Jori lächelte und sagte: Komm, Flimm. Wir schauen uns das gemeinsam an."
)
STYLE=(
    "Deutsch (Deutschland), warmes gemütliches Vorlesen am Kamin, "
    "wie eine liebevolle Großmutter ihren Enkeln eine spannende Geschichte erzählt. "
    "Ganz natürlich, weich, freundlich, vertraut und leicht schmunzelnd; "
    "lebendige Betonung, nicht schulmeisterlich, nicht steif, nicht geflüstert, "
    "gut hörbar, nicht übertrieben langsam; kein österreichischer Dialekt."
)
FILTER=(
    "highpass=f=135,"
    "equalizer=f=2800:t=q:w=1.2:g=2.1,"
    "acompressor=threshold=0.090:ratio=2.4:attack=9:release=150:makeup=1.5,"
    "loudnorm=I=-12:TP=-0.9:LRA=5"
)
OUT=Path("voice_auditions")


def generate(voice, secret):
    request={
        "model":MODEL,
        "input":[{
            "type":"user_input",
            "content":[{
                "type":"text",
                "text":TRANSCRIPT,
                "annotations":[{"type":"speech_metadata","style":STYLE}]
            }]
        }],
        "response_format":{"type":"audio"},
        "generation_config":{"speech_config":[{"voice":voice}]}
    }
    url="https://generativelanguage.googleapis.com/v1beta/interactions"
    req=urllib.request.Request(url,
        data=json.dumps(request,ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Content-Type":"application/json","x-goog-api-key":secret,
                 "User-Agent":"Jori-Flimm-VoiceAudition/1.0"})
    try:
        with urllib.request.urlopen(req,timeout=95) as r:
            content=json.load(r)
    except urllib.error.HTTPError as exc:
        # Avoid logging server response which may echo sensitive request metadata.
        raise RuntimeError(f"Gemini {voice}: HTTP {exc.code} (no voice generated)") from exc
    audio=[]
    for step in content.get("steps",[]):
        for part in step.get("content",[]):
            if part.get("type")=="audio" and part.get("data"):
                audio.append(part["data"])
    if not audio:
        raise RuntimeError(f"Gemini {voice}: no audio found in response")
    raw=base64.b64decode(audio[-1],validate=True)
    if len(raw)<5000 or len(raw)>25_000_000:
        raise RuntimeError(f"Gemini {voice}: abnormal WAV size")
    wav=OUT/(voice+"_raw.wav")
    wav.write_bytes(raw)
    probe=subprocess.check_output(["ffprobe","-v","error","-show_entries",
         "format=duration:stream=codec_name,sample_rate,channels",
         "-of","json",str(wav)],text=True)
    data=json.loads(probe)
    duration=float(data["format"]["duration"])
    if duration<5 or duration>50:
        raise RuntimeError(f"Gemini {voice}: unexpected duration {duration:.1f}")
    # Create a mono audio-first file to rule out handset MP4 player/mixer errors.
    dst=OUT/(voice+"_Omi_Hoerprobe_LAUT.mp3")
    subprocess.run(["ffmpeg","-nostdin","-hide_banner","-v","error","-y",
        "-i",str(wav),"-vn","-af",FILTER,"-ac","1","-ar","48000",
        "-c:a","libmp3lame","-b:a","160k",str(dst)],
        check=True,timeout=60)
    if dst.stat().st_size<30000:
        raise RuntimeError(f"Gemini {voice}: MP3 seems empty")
    return {"name":voice,"duration_seconds":round(duration,2),"mp3":str(dst),
            "source":"Gemini 3.8 Flash TTS","sample":TRANSCRIPT,
            "status":"preview_unapproved_not_published"}


def main():
    api_key=os.getenv("JORI_GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GitHub Secret JORI_GEMINI_API_KEY missing")
    OUT.mkdir(parents=True,exist_ok=True)
    done=[]
    for voice in VOICES:
        try:
            result=generate(voice,api_key)
            done.append(result)
            print(f"STORY_VOICE_SAMPLE_OK {voice} {result['duration_seconds']}s",flush=True)
        except Exception as exc:
            print(f"STORY_VOICE_SAMPLE_FAILED {voice}: {exc}",file=sys.stderr,flush=True)
    (OUT/"manifest.json").write_text(json.dumps(
        {"publish_approved":False,"voices":done,"target":"warm German grandmother voice",
         "loudness_target_lufs":-12,"not_proof_of_actual_phone_speaker_volume":True},
        ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if not done:
        raise RuntimeError("No free-tier sample was generated")
    print(f"VOICE_AUDITION_COMPLETE successful={len(done)}; no production change")


if __name__=="__main__":
    try: main()
    except Exception as exc:
        print(f"VOICE_AUDITION_FATAL {exc}",file=sys.stderr)
        sys.exit(1)
