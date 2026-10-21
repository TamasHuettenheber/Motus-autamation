#!/usr/bin/env python3
"""One episode's Sulafat narration for the five-episode STORY PREVIEW batch.

All results are unpublished. Only original stories from relaunch-v2 are used.
"""
import argparse,json,shutil,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
SEASON=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--episode",type=int,required=True,choices=[1,2,3,4,5])
    args=p.parse_args()
    data=json.loads((SEASON/"staffel1_folgen_001_005.json").read_text(encoding="utf-8"))
    epi=next(x for x in data["episodes"] if int(x["episode_number"])==args.episode)
    if epi["series_version"]!="relaunch-v2" or epi["approved_for_publish"] is not False:
        raise ValueError("Unapproved relaunch episode required")
    if epi["voice"]["speaker_id"]!="Sulafat" or epi["narration"].count("[[PAUSE:7]]")!=1:
        raise ValueError("Wrong narrator or wrong riddle pause")
    work=Path("work")
    work.mkdir(exist_ok=True)
    epi["voice"]["model"]=__import__("os").environ.get("JORI_TTS_MODEL","gemini-3.8-flash-tts")
    (work/"payload.json").write_text(json.dumps({
       "narration":epi["narration"],
       "voice":epi["voice"]
    },ensure_ascii=False),encoding="utf-8")
    subprocess.run([sys.executable,"kids/jori-flimm/scripts/generate_voice_gemini.py"],
                   check=True,timeout=400)
    prefix=f"folge_{args.episode:03d}"
    out=Path("out/audio")
    out.mkdir(parents=True,exist_ok=True)
    source=work/"narration_source.wav"
    shutil.copy2(source,out/f"{prefix}.wav")
    shutil.copy2(work/"voice-timeline.json",out/f"{prefix}_timeline.json")
    subprocess.run(["ffmpeg","-nostdin","-y","-v","error",
       "-i",str(source),"-af",
       "highpass=f=110,acompressor=threshold=0.08:ratio=2.5:attack=10:release=170,loudnorm=I=-13:TP=-1.5:LRA=4",
       "-ar","48000","-ac","1","-c:a","libmp3lame","-b:a","160k",
       str(out/f"{prefix}.mp3")],check=True,timeout=120)
    info=json.loads((out/f"{prefix}_timeline.json").read_text(encoding="utf-8"))
    print(f"SULAFAT_AUDIO_OK EP={args.episode:03d} seconds={info['duration']} no TikTok")
if __name__=="__main__":
    try:main()
    except Exception as exc:
        print(f"SULAFAT_AUDIO_BLOCKED: {exc}",file=sys.stderr)
        sys.exit(1)
