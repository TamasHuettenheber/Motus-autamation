#!/usr/bin/env python3
"""Rebuild Jori & Flimm episode 001 from versioned GitHub art and Sulafat audio."""
import math
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
 im=Image.open((R/"kids/jori-flimm/assets/e001/scene-01.png") if i in (3,4) else (A/img)).convert("RGB").resize((720,1280));d=ImageDraw.Draw(im)
 d.rounded_rectangle((30,30,382,79),radius=15,fill="#11284e")
 d.text((48,43),"JORI & FLIMM  •  FOLGE 001",font=ImageFont.truetype(font,20),fill="#fff1d0")
 if i in (3,4):
  # Faithful illustrated wooden moon/sun/star puzzle used in approved V10.
  for n,(x,label) in enumerate([(135,"MOND"),(359,"SONNE"),(583,"STERN")]):
   y=525
   d.rounded_rectangle((x-11,y+42,x+11,y+176),radius=5,fill=(115,76,45))
   d.rounded_rectangle((x-89,y-73,x+89,y+50),radius=16,fill=(57,34,26))
   d.rounded_rectangle((x-83,y-67,x+83,y+43),radius=12,fill=(175,116,68))
   if i==4 and n==2:d.rounded_rectangle((x-89,y-73,x+89,y+50),radius=15,outline=(255,239,146),width=7)
   if n==0:
    d.ellipse((x-29,y-49,x+26,y+8),fill=(255,232,141))
    d.ellipse((x-9,y-59,x+38,y-5),fill=(175,116,68))
   elif n==1:
    d.ellipse((x-22,y-39,x+22,y+5),fill=(255,232,141))
    for k in range(12):
     a=k*2*math.pi/12
     d.line((x+math.cos(a)*31,y-17+math.sin(a)*31,x+math.cos(a)*40,y-17+math.sin(a)*40),fill=(255,232,141),width=4)
   else:
    xy=[]
    for k in range(10):
     a=-math.pi/2+k*math.pi/5;rr=33 if k%2==0 else 15.51
     xy.append((x+math.cos(a)*rr,y-16+math.sin(a)*rr))
    d.polygon(xy,fill=(255,232,141))
   d.text((x,y+15),label,font=ImageFont.truetype(font,16),anchor="mm",fill="#fff0d8",stroke_width=1,stroke_fill="#5a3929")
 pic=W/f"scene{i}.png";im.save(pic);clip=W/f"scene{i}.mp4"
 run("ffmpeg","-nostdin","-y","-loglevel","error","-loop","1","-framerate","24","-i",pic,"-t",f"{t:.3f}","-vf","zoompan=z='min(zoom+0.00018,1.045)':d=1:fps=24:s=720x1280,format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","23","-r","24",clip)
 clips.append(clip)
lst=W/"concat.txt";lst.write_text("".join("file '"+str(p.resolve())+"'\n" for p in clips))
visual=W/"visual.mp4"
run("ffmpeg","-nostdin","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-c","copy",visual)
audio=W/"audio.wav"
run("ffmpeg","-nostdin","-y","-loglevel","error","-i",voice,"-i",story,"-filter_complex","[0:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono[a0];[1:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono[a1];[a0][a1]concat=n=2:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=5[a]","-map","[a]","-c:a","pcm_s16le",audio)
# Restore original timed V7 captions at their V10-shifted positions.
def stamp(t):
 h=int(t//3600);m=int(t%3600//60);return f"{h}:{m:02d}:{t%60:05.2f}"
header="""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
ScaledBorderAndShadow: yes
WrapStyle: 2
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Child,DejaVu Sans,36,&H00FFFFFF,&H00FFFFFF,&HDD04203C,&H00000000,1,0,0,0,100,100,0,0,1,3.8,0.6,2,38,38,282,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
rows=(R/"kids/jori-flimm/relaunch-v2/episode001_v10_caption_timeline.txt").read_text().splitlines()
assert len(rows)>25
for row in rows:
 a,b,txt=row.split("|",2)
 a=float(a)+D-3.75;b=float(b)+D-3.75
 assert 0<a<b<D+90
 header+=f"Dialogue: 0,{stamp(a)},{stamp(b)},Child,,0,0,0,,{txt}\n"
captions=W/"captions.ass";captions.write_text(header,encoding="utf-8")
run("ffmpeg","-nostdin","-y","-loglevel","error","-i",visual,"-i",audio, "-filter_complex",f"[0:v]ass={captions}[v]","-map","[v]","-map","1:a","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-r","24","-c:a","aac","-b:a","192k","-movflags","+faststart","-shortest",P)
assert P.stat().st_size>1_000_000 and 90<duration(P)<115
print("GITHUB_RENDER_DONE",P,duration(P),P.stat().st_size)
