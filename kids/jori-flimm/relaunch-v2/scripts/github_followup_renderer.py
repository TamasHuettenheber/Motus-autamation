#!/usr/bin/env python3
"""Render episodes 002–005 on GitHub, using story-specific puzzles and original illustrated characters."""
import argparse,json,math,re,subprocess,os,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
ROOT=Path.cwd()
BASE=ROOT/"kids/jori-flimm/relaunch-v2"
parser=argparse.ArgumentParser();parser.add_argument("--episode",type=int,required=True,choices=[2,3,4,5]);args=parser.parse_args()
n=args.episode
ART=ROOT/f"kids/jori-flimm/assets/e{n:03d}"
episode=next(e for e in json.loads((BASE/"staffel1_folgen_001_005.json").read_text())["episodes"] if e["episode_number"]==n)
W=ROOT/f"work/episode_{n:03d}";W.mkdir(parents=True,exist_ok=True)
audio=W/"narration_source.wav";timeline=W/"voice-timeline.json"
assert audio.exists() and timeline.exists(),"No validated Sulafat narration"
t=json.loads(timeline.read_text());items=t["items"]
assert len(items)==3 and items[1]["kind"]=="pause" and abs(items[1]["duration"]-7)<0.12
D=t["duration"];assert 45<D<150
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F2="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font=lambda size,bold=True:ImageFont.truetype(F if bold else F2,size)
def cmd(*args):subprocess.run(list(map(str,args)),check=True,timeout=500)
def draw_scene(name,section):
 im=Image.open(ART/"scene.jpg").convert("RGB").resize((720,1280))
 overlay=Image.new("RGBA",(720,1280),(0,0,0,0));d=ImageDraw.Draw(overlay)
 d.rounded_rectangle((34,38,683,102),radius=17,fill=(15,37,67,196))
 d.text((55,57),f"JORI & FLIMM   ·   FOLGE {n:03d}",font=font(23),fill="#fff2cf")
 if section=="hook":
  d.rounded_rectangle((40,155,680,253),radius=20,fill=(16,37,62,200))
  d.text((360,202),episode["title"],font=font(25),anchor="mm",fill="white",stroke_width=1,stroke_fill="#1e354f")
 if section=="puzzle" or section=="answer":
  d.rounded_rectangle((38,470,682,774),radius=23,fill=(18,37,63,232),outline=(242,205,119,240),width=4)
  d.text((360,500),"DAS RÄTSEL",font=font(26),anchor="mt",fill="#ffe4a3")
  if n==2:
   colors=["#78c9ff","#ffd36a","#78c9ff","#ffd36a" if section=="answer" else "#ffffff"]
   for i,x in enumerate([150,290,430,570]):
    d.ellipse((x-41,578,x+41,660),fill=colors[i],outline="#e9f3ff",width=4)
    d.text((x,687),["BLAU","GOLD","BLAU","GOLD" if section=="answer" else "?"][i],font=font(17),anchor="mt",fill="white")
  elif n==3:
   for i,x in enumerate([150,290,430,570]):
    d.rounded_rectangle((x-49,578,x+49,667),radius=16,fill=(126,153,173,255),outline="#d5ebfc",width=3)
    d.text((x,619),["2","4","6","8" if section=="answer" else "?"][i],font=font(47),anchor="mm",fill="#fff5cc")
  elif n==4:
   for i,x in enumerate([150,360,570]):
    d.rounded_rectangle((x-71,575,x+71,698),radius=18,fill="#996c44",outline="#ffe6a6",width=3)
    if i==0:d.ellipse((x-21,606,x+21,648),fill="#ffdc88")
    if i==1:d.polygon([(x,601),(x-26,649),(x+26,649)],fill="#ffdc88")
    if i==2:d.rectangle((x-21,606,x+21,648),fill="#ffdc88")
    if section=="answer" and i==1:d.rounded_rectangle((x-77,570,x+77,705),radius=19,outline="#fff29a",width=7)
   d.text((360,719),"KREIS     DREIECK     QUADRAT",font=font(19),anchor="mm",fill="white")
  else:
   for i,x in enumerate([155,295,435,575]):
    if i<3 or section=="answer":d.ellipse((x-29,584,x+29,642),fill="#ffe09a",outline="#fff8dc",width=5)
    else:d.ellipse((x-29,584,x+29,642),outline="#fff8dc",width=5)
   d.text((360,694),"WIE VIELE LEUCHTEN?",font=font(23),anchor="mm",fill="white")
 if section=="cliff":
  d.rounded_rectangle((40,178,680,254),radius=16,fill=(13,31,61,218))
  d.text((360,213),"WIE GEHT ES WEITER?",font=font(27),anchor="mm",fill="#ffebbc")
 return Image.alpha_composite(im.convert("RGBA"),overlay).convert("RGB")
for section in ["hook","story","puzzle","answer","cliff"]:
 draw_scene(n,section).save(W/f"{section}.png")
before=items[0]["duration"];pause=items[1]["duration"];after=items[2]["duration"]
# Four story phases: title/hook, story, full seven-second thinking time, answer and cliffhanger.
segments=[("hook",min(8,before*.19)),("story",before-min(8,before*.19)),("puzzle",pause),("answer",after*.68),("cliff",after*.32)]
clips=[]
for i,(name,dur) in enumerate(segments):
 clip=W/f"seg_{i}.mp4"
 cmd("ffmpeg","-nostdin","-y","-loglevel","error","-loop","1","-framerate","24","-i",W/f"{name}.png","-t",f"{dur:.3f}","-vf","zoompan=z='min(zoom+0.00018,1.045)':d=1:fps=24:s=720x1280,format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","23","-r","24",clip)
 clips.append(clip)
concat=W/"concat.txt";concat.write_text("".join("file '"+str(p.resolve())+"'\n" for p in clips))
video=W/"video.mp4";cmd("ffmpeg","-nostdin","-y","-loglevel","error","-f","concat","-safe","0","-i",concat,"-c","copy",video)
def ts(t):return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
header="""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
ScaledBorderAndShadow: yes
WrapStyle: 2
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Child,DejaVu Sans,35,&H00FFFFFF,&H00FFFFFF,&HDD04203C,&H00000000,1,0,0,0,100,100,0,0,1,3.8,0.6,2,38,38,277,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
def emit(a,b,txt):
 global header
 txt=txt.replace("\n"," ").strip()
 if not txt:return
 words=txt.split()
 lines=[];line=""
 for word in words:
  trial=(line+" "+word).strip()
  if line and font(35).getlength(trial)>610:lines.append(line);line=word
  else:line=trial
 if line:lines.append(line)
 groups=[lines[i:i+2] for i in range(0,len(lines),2)]
 weights=[max(1,len(" ".join(g))) for g in groups];total=sum(weights);start=a
 for i,(group,weight) in enumerate(zip(groups,weights)):
  end=b if i==len(groups)-1 else start+(b-a)*weight/sum(weights[i:])
  if end-start>.08:
   rendered="\\N".join(group)
   header+=f"Dialogue: 0,{ts(start)},{ts(end)},Child,,0,0,0,,{rendered}\n"
  start=end
for item in [items[0],items[2]]:
 txt=item["text"].strip()
 # sentence-aware captions; use the exact TTS segment transcript, not stale story JSON.
 pieces=re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ„])",txt)
 pieces=[p for p in pieces if p.strip()]
 weights=[max(2,len(p)) for p in pieces];total=sum(weights);cur=item["start"]
 for i,(p,w) in enumerate(zip(pieces,weights)):
  end=item["end"] if i==len(pieces)-1 else cur+(item["end"]-cur)*w/sum(weights[i:])
  emit(cur,end,p);cur=end
emit(items[1]["start"],items[1]["end"],episode["question"])
sub=W/"captions.ass";sub.write_text(header)
output=ROOT/f"published/jori-flimm-2026-10-{22+n-1:02d}-e{n:03d}.mp4";output.parent.mkdir(exist_ok=True)
cmd("ffmpeg","-nostdin","-y","-loglevel","error","-i",video,"-i",audio,"-filter_complex",f"[0:v]ass={sub}[v]","-map","[v]","-map","1:a","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-r","24","-c:a","aac","-b:a","192k","-movflags","+faststart","-shortest",output)
assert output.stat().st_size>1_000_000
print(f"JORI_EPISODE_RENDER_OK episode={n} duration={D} bytes={output.stat().st_size}")
