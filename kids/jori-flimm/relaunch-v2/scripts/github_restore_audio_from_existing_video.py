#!/usr/bin/env python3
"""Recover current Sulafat audio from the scheduled MP4 without new TTS."""
import argparse,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--episode",type=int,required=True,choices=[2,3,4,5]);n=p.parse_args().episode
root=Path.cwd();d=22+n-1;source=root/f"work/episode_{n:03d}/original-scheduled.mp4"
work=source.parent;work.mkdir(parents=True,exist_ok=True);raw=work/"source-audio.wav";audio=work/"narration_source.wav";timeline=work/"voice-timeline.json"
original="dbcbe1cc8c648bf8cbdf9bfcd9d28ac15128ef50"
subprocess.run(["git","fetch","--depth=1","origin",original],check=True,timeout=90)
old_path=f"published/jori-flimm-2026-10-{d:02d}-e{n:03d}.mp4"
old_video=subprocess.run(["git","show",f"{original}:{old_path}"],check=True,stdout=subprocess.PIPE,timeout=60).stdout
assert len(old_video)>1_000_000,f"Original production MP4 missing in {original}:{old_path}"
source.write_bytes(old_video)
def run(*args):return subprocess.run(list(map(str,args)),check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=180)
run("ffmpeg","-nostdin","-y","-loglevel","error","-i",source,"-vn","-ac","1","-ar","24000","-c:a","pcm_s16le",raw)
dur=float(json.loads(run("ffprobe","-v","error","-show_entries","format=duration","-of","json",raw).stdout)["format"]["duration"])
log=run("ffmpeg","-nostdin","-i",raw,"-af","silencedetect=noise=-25dB:d=5","-f","null","-").stderr
starts=[float(x) for x in re.findall(r"silence_start: ([0-9.]+)",log)];ends=[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",log)]
pairs=[]
for s in starts:
 es=[e for e in ends if e>s]
 if es and 7<=es[0]-s<=20 and s>10 and dur-es[0]>10:pairs.append((s,es[0]))
assert len(pairs)==1,f"Expected one long puzzle pause, found {pairs}"
s,e=pairs[0]
data=json.loads((root/"kids/jori-flimm/relaunch-v2/staffel1_folgen_001_005.json").read_text(encoding="utf-8"))
ep=next(x for x in data["episodes"] if x["episode_number"]==n);narr=ep["narration"];assert narr.count("[[PAUSE:7]]")==1
before,after=narr.split("[[PAUSE:7]]")
fix=lambda x:x.replace("flüsterte er.","flüsterte sie.").replace("sagte er.","sagte sie.").replace("Jori bot seine Hilfe an","Jori bot ihre Hilfe an")
before,after=fix(before),fix(after);cut=s+7
run("ffmpeg","-nostdin","-y","-loglevel","error","-i",raw,"-filter_complex",f"[0:a]atrim=start=0:end={s:.6f},asetpts=PTS-STARTPTS[a];anullsrc=r=24000:cl=mono,atrim=duration=7,asetpts=PTS-STARTPTS[p];[0:a]atrim=start={e:.6f}:end={dur:.6f},asetpts=PTS-STARTPTS[b];[a][p][b]concat=n=3:v=0:a=1[out]","-map","[out]","-c:a","pcm_s16le",audio)
total=s+7+(dur-e);items=[{"kind":"speech","text":before.strip(),"start":0.0,"end":s,"duration":s},{"kind":"pause","text":"","start":s,"end":s+7,"duration":7.0},{"kind":"speech","text":after.strip(),"start":s+7,"end":total,"duration":dur-e}]
timeline.write_text(json.dumps({"duration":total,"items":items,"voice":"Sulafat","source":"existing scheduled MP4; no TTS regeneration"},ensure_ascii=False),encoding="utf-8")
print(f"JORI_EXISTING_SULAFAT_AUDIO_REUSED episode={n} detected_pause={e-s:.3f}s normalized=7.000s duration={total:.3f}s")
