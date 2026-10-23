#!/usr/bin/env python3
"""One-off Jori & Flimm introduction trailer. Isolated from episodes and MOTUS."""
import base64
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import wave

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path.cwd()
WORK=ROOT/"work/jori_trailer_20261023"
WORK.mkdir(parents=True,exist_ok=True)
OUT=ROOT/"published/jori-flimm-trailer-2026-10-23.mp4"
OUT.parent.mkdir(exist_ok=True)
VOICE_TEXT=(
  "Psst! Hast du das Leuchten gesehen? "
  "Ich bin Jori! Und ich bin Flimm! "
  "In unserer Welt gibt es geheimnisvolle Türen, funkelnde Laternen "
  "und Rätsel, die wir nur gemeinsam lösen können. "
  "Jeden Tag wartet ein neues Stück unserer Geschichte auf dich. "
  "Bist du bereit? Dann folge Jori und Flimm, "
  "damit du kein Abenteuer verpasst!"
)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
ART=[
 ROOT/"kids/jori-flimm/assets/e001/scene-01.png",
 ROOT/"kids/jori-flimm/assets/e002/scene-01.jpg",
 ROOT/"kids/jori-flimm/assets/e002/scene-02.jpg",
 ROOT/"kids/jori-flimm/assets/e002/scene-04.jpg",
 ROOT/"kids/jori-flimm/assets/e002/scene-05.jpg",
]
SCENES=[
 ("PSST!","Hast du das Leuchten gesehen?"),
 ("WIR SIND JORI & FLIMM","Zwei Freunde. Ein großes Abenteuer."),
 ("MAGISCHE GEHEIMNISSE","Funkelnde Laternen und verborgene Türen"),
 ("DU RÄTSELST MIT!","Gemeinsam lösen wir jedes Geheimnis."),
 ("VERPASSE KEINE FOLGE!","Folge @jori.flimm"),
]
def run(*argv):
  subprocess.run(list(map(str,argv)),check=True,timeout=300)
def probe(f):
  return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(f)],text=True).strip())
def font(size,bold=True):
  return ImageFont.truetype(FONT if bold else FONTR,size)
def wrap(draw,text,f,max_width):
  result=[];line=""
  for word in text.split():
    test=(line+" "+word).strip()
    if line and draw.textlength(test,font=f)>max_width:
      result.append(line);line=word
    else:line=test
  if line:result.append(line)
  return result
def image_for_scene(index):
  image=Image.open(ART[index]).convert("RGB").resize((720,1280),Image.Resampling.LANCZOS)
  dr=ImageDraw.Draw(image,"RGBA")
  dr.rounded_rectangle((33,40,688,110),radius=18,fill=(13,32,61,205))
  dr.text((360,75),"JORI & FLIMM   ·   UNSERE WELT",font=font(24),anchor="mm",
          fill="#ffedc9",stroke_width=1,stroke_fill="#142744")
  dr.rounded_rectangle((40,832,680,1038),radius=30,fill=(11,29,54,215),
                       outline=(255,216,143,210),width=3)
  title,subtitle=SCENES[index]
  title_font=font(31 if index!=4 else 30)
  dr.text((360,885),title,font=title_font,anchor="mm",fill="#ffe7ab",
          stroke_width=1,stroke_fill="#142744")
  subfont=font(26,False)
  rows=wrap(dr,subtitle,subfont,574)
  for j,line in enumerate(rows[:3]):
    dr.text((360,955+j*35),line,font=subfont,anchor="mm",fill="white")
  if index==4:
    dr.rounded_rectangle((155,1075,565,1150),radius=25,fill=(255,213,109,245))
    dr.text((360,1113),"JETZT FOLGEN  +",font=font(28),anchor="mm",fill="#172d4c")
  return image
def main():
  assert all(x.is_file() for x in ART),"Five versioned Jori art assets required"
  secret=os.environ.get("JORI_GEMINI_API_KEY","").strip()
  assert secret,"JORI_GEMINI_API_KEY missing"
  # Reuse the approved existing Gemini/Sulafat voice helper; no alternative paid vendor.
  sys.path.insert(0,str(ROOT/"kids/jori-flimm/scripts"))
  from generate_voice_gemini import tts_segment
  voice=WORK/"narration.wav"
  voice.write_bytes(tts_segment(VOICE_TEXT,"Sulafat",secret))
  raw_len=probe(voice)
  assert 15<raw_len<47,f"Unexpected Sulafat duration: {raw_len}"
  # Natural spoken audio lightly retimed to a consistent 28s TikTok format.
  DUR=28.0
  adjusted=WORK/"voice_28.wav"
  run("ffmpeg","-nostdin","-y","-v","error","-i",voice,
      "-af",f"atempo={raw_len/DUR:.5f},aresample=24000,apad=pad_dur=0.2",
      "-t",str(DUR),"-ar","24000","-ac","1","-c:a","pcm_s16le",adjusted)
  assert abs(probe(adjusted)-DUR)<.08
  # Quiet original synthesized music bed, mixed under the narration.
  music=WORK/"magic_bed.wav"
  with wave.open(str(music),"wb") as w:
    rate=24000;w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate)
    block=bytearray()
    for k in range(int(DUR*rate)):
      t=k/rate
      chord=(196.00,246.94,293.66,392.0)
      val=sum(math.sin(2*math.pi*f*t+math.sin(t*.42)*.3) for f in chord)/len(chord)
      pulse=0.65+0.35*math.sin(2*math.pi*t/4)**2
      sample=int(1100*pulse*val)
      block.extend(sample.to_bytes(2,"little",signed=True))
    w.writeframes(bytes(block))
  combined=WORK/"audio.wav"
  run("ffmpeg","-nostdin","-y","-v","error","-i",adjusted,"-i",music,
      "-filter_complex","[0:a]volume=1.0[a];[1:a]volume=0.8[b];[a][b]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.94[out]",
      "-map","[out]","-ar","24000","-ac","1","-c:a","pcm_s16le",combined)
  assert abs(probe(combined)-DUR)<.1
  segments=[]
  for i in range(5):
    pic=WORK/f"scene_{i:02d}.png"
    image_for_scene(i).save(pic)
    clip=WORK/f"clip_{i:02d}.mp4"
    # Five distinct images, mild Ken Burns motion, vertical 9:16.
    run("ffmpeg","-nostdin","-y","-v","error","-loop","1","-framerate","24",
        "-i",pic,"-t","5.6","-vf",
        "zoompan=z='min(zoom+0.00025,1.06)':d=1:fps=24:s=720x1280,format=yuv420p",
        "-c:v","libx264","-preset","ultrafast","-crf","23","-r","24",clip)
    segments.append(clip)
  manifest=WORK/"concat.txt"
  manifest.write_text("".join("file '"+str(x.resolve())+"'\n" for x in segments),encoding="utf-8")
  visual=WORK/"visual.mp4"
  run("ffmpeg","-nostdin","-y","-v","error","-f","concat","-safe","0",
      "-i",manifest,"-c","copy",visual)
  run("ffmpeg","-nostdin","-y","-v","error","-i",visual,"-i",combined,
      "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","160k",
      "-movflags","+faststart","-shortest",OUT)
  dur=probe(OUT)
  assert 27.7<dur<28.3,(dur,OUT)
  assert OUT.stat().st_size>1_000_000,"Invalidly small video"
  stream=subprocess.check_output(["ffprobe","-v","error","-show_entries",
       "stream=codec_name,width,height","-of","json",str(OUT)],text=True)
  info=json.loads(stream)
  assert any(s.get("codec_name")=="h264" and s.get("width")==720 and s.get("height")==1280 for s in info["streams"])
  assert any(s.get("codec_name")=="aac" for s in info["streams"])
  print("JORI_TRAILER_RENDER_QC_OK",json.dumps({"file":str(OUT),"duration":dur,"bytes":OUT.stat().st_size,
        "art_scenes":len(ART),"voice":"Sulafat","caption":"Folge @jori.flimm","audio":"AAC + original quiet music"},ensure_ascii=False))
if __name__=="__main__":main()
