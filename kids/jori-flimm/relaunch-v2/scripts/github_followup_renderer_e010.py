#!/usr/bin/env python3
"""Render Jori & Flimm follow-up episodes with story-matched, episode-specific art."""
import argparse,json,math,re,subprocess,os,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
ROOT=Path.cwd()
BASE=ROOT/"kids/jori-flimm/relaunch-v2"
parser=argparse.ArgumentParser();parser.add_argument("--episode",type=int,required=True,choices=[10]);args=parser.parse_args()
n=args.episode
ART=ROOT/"kids/jori-flimm/relaunch-v2/assets/episode-010-v1"
SCENE_EXT=".jpg"
SCENE_INDEX={"hook":1,"story_a":2,"story_b":3,"puzzle":4,"answer":5,"cliff":6}
SCENE_COUNT=6
scene_files=[ART/f"scene-{i:02d}{SCENE_EXT}" for i in range(1,SCENE_COUNT+1)]
assert all(p.is_file() for p in scene_files), "Missing episode-specific scene art"
print(f"JORI_SCENE_ART_READY episode={n} unique_scenes={SCENE_COUNT}")
episode=json.loads((BASE/"episode_010_story_draft.json").read_text(encoding="utf-8"))
W=ROOT/f"work/episode_{n:03d}";W.mkdir(parents=True,exist_ok=True)
audio=W/"narration_source.wav";timeline=W/"voice-timeline.json"
assert audio.exists() and timeline.exists(),"No validated Sulafat narration"
t=json.loads(timeline.read_text());items=t["items"]
pause_indices=[i for i,item in enumerate(items) if item["kind"]=="pause"]
assert len(pause_indices)==1 and abs(items[pause_indices[0]]["duration"]-7)<0.12
pause_index=pause_indices[0]
assert len(items)==6 and [item["kind"] for item in items]==["speech","speech","speech","pause","speech","speech"]
D=t["duration"];assert 45<D<150
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F2="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font=lambda size,bold=True:ImageFont.truetype(F if bold else F2,size)
def cmd(*args):subprocess.run(list(map(str,args)),check=True,timeout=500)
def draw_position_options(d,top,centers=None,half=82,label_size=16):
 centers=centers or [148,360,572]
 labels=["LINKS","MITTE","RECHTS"]
 for i,(x,label) in enumerate(zip(centers,labels)):
  d.rounded_rectangle((x-half,top,x+half,top+240),radius=18,fill=(43,62,88,250),outline=(230,218,185,245),width=3)
  if i==0: moon=(x,top+68); star=(x,top+157)
  elif i==1: star=(x-31,top+112); moon=(x+35,top+112)
  else: star=(x,top+68); moon=(x,top+157)
  moon_r=21 if half>70 else 16
  mx,my=moon;d.ellipse((mx-moon_r,my-moon_r,mx+moon_r,my+moon_r),fill="#ffe19a",outline="#fff7da",width=2)
  d.ellipse((mx-6,my-moon_r-4,mx+moon_r+5,my+moon_r-12),fill=(43,62,88,255))
  sx,sy=star;pts=[]
  for k in range(10):
   radius=(29 if half>70 else 21) if k%2==0 else (13 if half>70 else 9)
   angle=-math.pi/2+k*math.pi/5
   pts.append((sx+math.cos(angle)*radius,sy+math.sin(angle)*radius))
  d.polygon(pts,fill="#ffd76e",outline="#fff7da")
  d.text((x,top+218),label,font=font(label_size),anchor="mm",fill="white")
def draw_scene(name,section):
 im=Image.open(ART/f"scene-{SCENE_INDEX[section]:02d}{SCENE_EXT}").convert("RGB").resize((720,1280),Image.Resampling.LANCZOS)
 overlay=Image.new("RGBA",(720,1280),(0,0,0,0));d=ImageDraw.Draw(overlay)
 d.rounded_rectangle((34,38,683,102),radius=17,fill=(15,37,67,196))
 d.text((55,57),f"JORI & FLIMM   ·   FOLGE {n:03d}",font=font(23),fill="#fff2cf")
 if section=="hook":
  d.rounded_rectangle((40,155,680,253),radius=20,fill=(16,37,62,200))
  d.text((360,202),episode["title"],font=font(25),anchor="mm",fill="white",stroke_width=1,stroke_fill="#1e354f")
 if section=="puzzle":
  d.rounded_rectangle((38,142,682,224),radius=18,fill=(18,37,63,194),outline=(242,205,119,220),width=2)
  d.text((360,183),"WELCHE KUGEL LEUCHTET ZUERST?",font=font(21),anchor="mm",fill="#ffe4a3")
  d.rounded_rectangle((58,739,662,796),radius=14,fill=(18,37,63,202),outline=(242,205,119,210),width=2)
  d.text((360,768),"BLAU   →   SILBERN   →   GOLD",font=font(22),anchor="mm",fill="#fff3d0")
 if section=="answer":
  pass
 return Image.alpha_composite(im.convert("RGBA"),overlay).convert("RGB")
section_names=["hook","story_a","story_b","puzzle","answer","cliff"]
for section in section_names:
 draw_scene(n,section).save(W/f"{section}.png")
before=sum(item["duration"] for item in items[:pause_index] if item["kind"]=="speech")
pause=items[pause_index]["duration"]
after=sum(item["duration"] for item in items[pause_index+1:] if item["kind"]=="speech")
pre=items[:pause_index];post=items[pause_index+1:]
assert len(pre)==3 and len(post)==2
segments=[("hook",pre[0]["duration"]),("story_a",pre[1]["duration"]),("story_b",pre[2]["duration"]),("puzzle",pause),("answer",post[0]["duration"]),("cliff",post[1]["duration"])]
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
cues=[]
def emit(a,b,txt):
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
 weights=[max(1,len(" ".join(g))) for g in groups];start=a
 for i,(group,weight) in enumerate(zip(groups,weights)):
  end=b if i==len(groups)-1 else start+(b-start)*weight/sum(weights[i:])
  cues.append((start,end,"\\N".join(group)))
  start=end
for item in [item for item in items if item["kind"]=="speech"]:
 txt=item["text"].strip()
 pieces=re.split(r'(?<=[.!?])["»”]?\s+(?=[A-ZÄÖÜ„])',txt)
 pieces=[p for p in pieces if p.strip()]
 weights=[max(2,len(p)) for p in pieces];cur=item["start"]
 for i,(p,w) in enumerate(zip(pieces,weights)):
  end=item["end"] if i==len(pieces)-1 else cur+(item["end"]-cur)*w/sum(weights[i:])
  emit(cur,end,p);cur=end
cues.sort(key=lambda item:(item[0],item[1]))
pause_start=items[pause_index]["start"]
expected_words=re.findall(r"\w+"," ".join(item["text"] for item in items if item["kind"]=="speech").lower())
visible_words=[]
for i,(start,end,rendered) in enumerate(cues):
 if start<pause_start:end=min(end,pause_start)
 if i+1<len(cues):end=min(end,cues[i+1][0])
 if end-start>.08:
  header+=f"Dialogue: 0,{ts(start)},{ts(end)},Child,,0,0,0,,{rendered}\n"
  visible_words.extend(re.findall(r"\w+",rendered.replace("\\N"," ").lower()))
assert visible_words==expected_words, "Rendered subtitles omit, repeat, or reorder spoken words"
sub=W/"captions.ass";sub.write_text(header)
version_suffix="-v2"
output=ROOT/f"published/jori-flimm-2026-10-{22+n-1:02d}-e{n:03d}{version_suffix}.mp4";output.parent.mkdir(exist_ok=True)
cmd("ffmpeg","-nostdin","-y","-loglevel","error","-i",video,"-i",audio,"-filter_complex",f"[0:v]ass={sub}[v]","-map","[v]","-map","1:a","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-r","24","-c:a","aac","-b:a","192k","-movflags","+faststart","-shortest",output)
assert output.stat().st_size>1_000_000
rendered=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(output)],text=True).strip())
assert abs(rendered-D)<0.25,f"Rendered duration mismatch: expected {D}, got {rendered}"
print(f"JORI_EPISODE_RENDER_OK episode={n} duration={rendered} bytes={output.stat().st_size}")
