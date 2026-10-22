#!/usr/bin/env python3
"""Rebuild Jori & Flimm episode 001 from versioned GitHub art and Sulafat audio."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess
R=Path.cwd();W=R/"work/jori_v10";W.mkdir(parents=True,exist_ok=True)
A=R/"kids/jori-flimm/assets/e000";P=R/"published/jori-flimm-2026-10-22-e001.mp4";P.parent.mkdir(exist_ok=True)
def run(*args):subprocess.run(list(map(str,args)),check=True,timeout=500)
def duration(f):return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(f)],text=True))
voice=W/"Jori_001_Sulafat_Prolog_V10_Ihren_Namen.wav";story=W/"folge_001.wav"
assert voice.is_file() and story.is_file()
D=duration(voice)
font="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
small=ImageFont.truetype(font,29);large=ImageFont.truetype(font,35)
intro=[
("Mitten in einer Winternacht\nhörte Jori plötzlich ihren Namen.",.32,"scene-01.jpg"),
("Aber niemand war zu sehen.",.17,"scene-01.jpg"),
("Noch wusste sie nicht, dass sie gleich\nFlimm kennenlernen würde.",.28,"scene-02.jpg"),
("Hier beginnt ihre Geschichte:\nJori und Flimm. Folge eins.",.23,"scene-02.jpg")]
clips=[];pos=0
for i,(txt,w,img) in enumerate(intro):
 t=D-pos if i==3 else round(D*w,3)
 im=Image.open(A/img).convert("RGB").resize((720,1280));d=ImageDraw.Draw(im)
 if i==0:
  d.text((360,100),"JORI & FLIMM",font=large,anchor="mm",fill="white",stroke_width=3,stroke_fill="#26324a")
  d.text((360,153),"FOLGE 001",font=small,anchor="mm",fill="white",stroke_width=3,stroke_fill="#26324a")
 for j,line in enumerate(txt.split("\n")):d.text((360,850+j*50),line,font=small,anchor="mm",fill="white",stroke_width=3,stroke_fill="#29364b")
 pic=W/f"intro{i}.png";im.save(pic);clip=W/f"intro{i}.mp4"
 run("ffmpeg","-nostdin","-y","-loglevel","error","-loop","1","-framerate","24","-i",pic,"-t",f"{t:.3f}","-vf","format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","22","-r","24",clip)
 clips.append(clip);pos+=t
# Scene timings correspond to the existing V7 story retained by approved V10.
ends=[8.86,19.16,27.46,62.16,69.06,78.76,86.06]
names=["scene-01.jpg","scene-03.jpg","scene-04.jpg","scene-05.jpg","scene-05.jpg","scene-05.jpg","scene-06.jpg"]
previous=0
for i,(end,img) in enumerate(zip(ends,names)):
 t=end-previous;previous=end
 im=Image.open(A/img).convert("RGB").resize((720,1280));d=ImageDraw.Draw(im)
 d.rounded_rectangle((30,30,382,79),radius=15,fill="#11284e")
 d.text((48,43),"JORI & FLIMM  •  FOLGE 001",font=ImageFont.truetype(font,20),fill="#fff1d0")
 if i in (3,4):
  for x,label in [(137,"MOND"),(360,"SONNE"),(582,"STERN")]:
   d.rounded_rectangle((x-88,500,x+88,614),radius=17,fill="#ad7548",outline="#5a3929",width=6)
   d.text((x,560),label,font=ImageFont.truetype(font,20),anchor="mm",fill="#fff1ca")
 pic=W/f"scene{i}.png";im.save(pic);clip=W/f"scene{i}.mp4"
 run("ffmpeg","-nostdin","-y","-loglevel","error","-loop","1","-framerate","24","-i",pic,"-t",f"{t:.3f}","-vf","zoompan=z='min(zoom+0.00018,1.045)':d=1:fps=24:s=720x1280,format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","23","-r","24",clip)
 clips.append(clip)
lst=W/"concat.txt";lst.write_text("".join("file '"+str(p.resolve())+"'\n" for p in clips))
visual=W/"visual.mp4"
run("ffmpeg","-nostdin","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-c","copy",visual)
audio=W/"audio.wav"
run("ffmpeg","-nostdin","-y","-loglevel","error","-i",voice,"-i",story,"-filter_complex","[0:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono[a0];[1:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono[a1];[a0][a1]concat=n=2:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=5[a]","-map","[a]","-c:a","pcm_s16le",audio)
run("ffmpeg","-nostdin","-y","-loglevel","error","-i",visual,"-i",audio,"-map","0:v","-map","1:a","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-r","24","-c:a","aac","-b:a","192k","-movflags","+faststart","-shortest",P)
assert P.stat().st_size>1_000_000 and 90<duration(P)<115
print("GITHUB_RENDER_DONE",P,duration(P),P.stat().st_size)
