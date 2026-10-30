#!/usr/bin/env python3
"""Render Jori & Flimm episode 012 with TikTok-safe puzzle and subtitles."""
import argparse,json,math,re,subprocess,os,wave
from datetime import date,timedelta
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path.cwd();BASE=ROOT/'kids/jori-flimm/relaunch-v2'
p=argparse.ArgumentParser();p.add_argument('--episode',type=int,required=True,choices=[12]);a=p.parse_args();n=a.episode
ART=BASE/'assets/episode-012-v1';W=ROOT/'work/episode_012';W.mkdir(parents=True,exist_ok=True)
SCENES={name:i for i,name in enumerate(['hook','story_a','story_b','puzzle','answer','cliff_transition','cliff'],1)}
paths=[ART/f'scene-{i:02d}.jpg' for i in range(1,8)]
assert all(x.is_file() for x in paths);assert len({x.read_bytes() for x in paths})==7
print('JORI_SCENE_ART_READY episode=12 unique_scenes=7')
episode=json.loads((BASE/'episode_012_story_draft.json').read_text(encoding='utf-8'))
audio=W/'narration_source.wav';timeline=W/'voice-timeline.json'
assert audio.is_file() and timeline.is_file(),'No validated Sulafat narration'
t=json.loads(timeline.read_text());items=t['items'];expected=['speech','speech','speech','speech','pause','speech','speech']
assert [x['kind'] for x in items]==expected,items
pause_index=4;pause=items[pause_index];assert abs(pause['duration']-7)<0.001
D=t['duration'];assert 70<D<150
# Remove only an accidental TTS tail immediately before the explicit seven-second source silence.
previous=items[pause_index-1]
probe=subprocess.run(['ffmpeg','-hide_banner','-i',str(audio),'-af','silencedetect=noise=-60dB:d=6.5','-f','null','-'],capture_output=True,text=True)
starts=[float(x) for x in re.findall(r'silence_start:\s*([0-9.]+)',probe.stderr)]
durations=[float(x) for x in re.findall(r'silence_duration:\s*([0-9.]+)',probe.stderr)]
trim=0.0
for start,duration in zip(starts,durations):
 if previous['start']<=start<pause['start'] and duration>=7.05:trim=pause['start']-start;break
if trim>0.04:
 assert trim<0.75,trim
 with wave.open(str(audio),'rb') as src:params=src.getparams();frames=src.readframes(src.getnframes())
 assert (params.framerate,params.sampwidth,params.nchannels)==(24000,2,1)
 cut=round((pause['start']-trim)*24000);ps=round(pause['start']*24000);pf=7*24000;fb=2
 rebuilt=frames[:cut*fb]+frames[ps*fb:(ps+pf)*fb]+frames[(ps+pf)*fb:]
 tmp=str(audio)+'.tmp'
 with wave.open(tmp,'wb') as dst:dst.setparams(params);dst.writeframes(rebuilt)
 os.replace(tmp,audio);previous['duration']=round(previous['duration']-trim,6);previous['end']=round(previous['end']-trim,6)
 for item in items[pause_index:]:item['start']=round(item['start']-trim,6);item['end']=round(item['end']-trim,6)
 t['duration']=round(t['duration']-trim,6);timeline.write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
 print(f'JORI_E012_REMOVED_TTS_PAUSE_TAIL seconds={trim:.3f}')
D=t['duration'];pause=items[pause_index]
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';F2='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=lambda size,bold=True:ImageFont.truetype(F if bold else F2,size)
def cmd(*xs):subprocess.run(list(map(str,xs)),check=True,timeout=600)
def house(d,x,y,s=1.0):
 w=38*s;h=28*s
 d.rectangle((x-w/2,y-h/2,x+w/2,y+h/2),fill='#f4e6c8',outline='white',width=max(1,round(2*s)))
 d.polygon([(x-w*.65,y-h/2),(x,y-h*1.25),(x+w*.65,y-h/2)],fill='#d84a43',outline='white')
 d.rectangle((x-5*s,y,x+5*s,y+h/2),fill='#6b4935')
def willow(d,x,y,s=1.0):
 d.rectangle((x-3*s,y-2*s,x+3*s,y+19*s),fill='#b9cad0')
 d.ellipse((x-22*s,y-17*s,x+22*s,y+12*s),fill='#b7dce4',outline='white',width=max(1,round(2*s)))
 for dx in (-12,-5,5,12):d.line((x+dx*s,y,x+dx*1.4*s,y+22*s),fill='#dff7ff',width=max(1,round(2*s)))
def option_card(d,x,label,mode):
 d.rounded_rectangle((x-65,515,x+65,752),radius=17,fill=(28,54,82,250),outline=(245,216,145,255),width=3)
 d.text((x,548),label,font=font(22),anchor='mm',fill='white')
 if mode=='above':house(d,x,615,.8);willow(d,x,682,.8)
 elif mode=='right':willow(d,x-25,650,.72);house(d,x+28,650,.72)
 else:willow(d,x,615,.8);house(d,x,686,.8)
def draw_scene(section):
 im=Image.open(ART/f'scene-{SCENES[section]:02d}.jpg').convert('RGB').resize((720,1280),Image.Resampling.LANCZOS)
 ov=Image.new('RGBA',(720,1280),(0,0,0,0));d=ImageDraw.Draw(ov)
 # All important title text ends at x=540; x>=560 stays free for TikTok controls.
 d.rounded_rectangle((34,38,540,102),radius=17,fill=(15,37,67,210))
 d.text((55,57),f'JORI & FLIMM   ·   FOLGE {n:03d}',font=font(23),fill='#fff2cf')
 if section=='hook':
  d.rounded_rectangle((40,150,540,245),radius=20,fill=(16,37,62,218))
  d.text((290,197),episode['title'],font=font(25),anchor='mm',fill='white')
 if section=='puzzle':
  d.rounded_rectangle((42,132,540,802),radius=26,fill=(13,32,56,242),outline=(246,211,127,255),width=4)
  d.text((291,182),'WELCHE KARTE STIMMT?',font=font(25),anchor='mm',fill='#fff2c9')
  # Reference arrangement: house above willow.
  d.rounded_rectangle((220,238,362,450),radius=18,fill=(28,54,82,250),outline=(112,205,244,255),width=3)
  house(d,291,300,1.0);willow(d,291,380,1.0)
  option_card(d,126,'A','above');option_card(d,291,'B','right');option_card(d,456,'C','below')
 return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
for section in SCENES:draw_scene(section).save(W/f'{section}.png')
def sentence_intervals(item):
 pieces=[x for x in re.split(r'(?<=[.!?])["»”]?\s+(?=[A-ZÄÖÜ„])',item['text'].strip()) if x.strip()]
 weights=[max(2,len(x)) for x in pieces];cur=item['start'];out=[]
 for i,(piece,weight) in enumerate(zip(pieces,weights)):
  end=item['end'] if i==len(pieces)-1 else cur+(item['end']-cur)*weight/sum(weights[i:])
  out.append((cur,end,piece));cur=end
 return out
pre=items[:pause_index];post=items[pause_index+1:];assert len(pre)==4 and len(post)==2
cliff_intervals=sentence_intervals(post[1]);red_start=next(a for a,b,s in cliff_intervals if s.startswith('In ihrem Dachfenster'))
segments=[('hook',pre[0]['duration']),('story_a',pre[1]['duration']),('story_b',pre[2]['duration']),
 ('puzzle',pre[3]['duration']+pause['duration']),('answer',post[0]['duration']),
 ('cliff_transition',red_start-post[1]['start']),('cliff',post[1]['end']-red_start)]
cursor=0;scene_timing=[]
for name,dur in segments:scene_timing.append({'scene':name,'start':round(cursor,3),'end':round(cursor+dur,3),'duration':round(dur,3)});cursor+=dur
(W/'scene-timing.json').write_text(json.dumps(scene_timing,ensure_ascii=False,indent=2)+'\n')
assert abs(scene_timing[3]['end']-pause['end'])<0.01;assert abs(scene_timing[6]['start']-red_start)<0.01
clips=[]
for i,(name,dur) in enumerate(segments):
 clip=W/f'seg_{i}.mp4';cmd('ffmpeg','-nostdin','-y','-loglevel','error','-loop','1','-framerate','24','-i',W/f'{name}.png','-t',f'{dur:.3f}','-vf',"zoompan=z='min(zoom+0.00018,1.045)':d=1:fps=24:s=720x1280,format=yuv420p",'-c:v','libx264','-preset','ultrafast','-crf','23','-r','24',clip);clips.append(clip)
concat=W/'concat.txt';concat.write_text(''.join("file '"+str(x.resolve())+"'\n" for x in clips))
video=W/'video.mp4';cmd('ffmpeg','-nostdin','-y','-loglevel','error','-f','concat','-safe','0','-i',concat,'-c','copy',video)
def ts(x):return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
header='''[Script Info]\nScriptType: v4.00+\nPlayResX: 720\nPlayResY: 1280\nScaledBorderAndShadow: yes\nWrapStyle: 2\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\nStyle: Child,DejaVu Sans,34,&H00FFFFFF,&H00FFFFFF,&HDD04203C,&H00000000,1,0,0,0,100,100,0,0,1,3.8,0.6,2,60,180,277,1\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n'''
cues=[]
def emit(a,b,txt):
 words=txt.replace('\n',' ').strip().split();lines=[];line=''
 for word in words:
  trial=(line+' '+word).strip()
  if line and font(34).getlength(trial)>450:lines.append(line);line=word
  else:line=trial
 if line:lines.append(line)
 groups=[lines[i:i+2] for i in range(0,len(lines),2)];weights=[max(1,len(' '.join(g))) for g in groups];start=a
 for i,(group,w) in enumerate(zip(groups,weights)):
  end=b if i==len(groups)-1 else start+(b-start)*w/sum(weights[i:]);cues.append((start,end,'\\N'.join(group)));start=end
for item in (x for x in items if x['kind']=='speech'):
 for a,b,piece in sentence_intervals(item):emit(a,b,piece)
cues.sort();expected_words=re.findall(r'\w+',' '.join(x['text'] for x in items if x['kind']=='speech').lower());visible=[]
for i,(a,b,rendered) in enumerate(cues):
 if a<pause['start']:b=min(b,pause['start'])
 if i+1<len(cues):b=min(b,cues[i+1][0])
 if b-a>.08:header+=f'Dialogue: 0,{ts(a)},{ts(b)},Child,,0,0,0,,{rendered}\n';visible.extend(re.findall(r'\w+',rendered.replace('\\N',' ').lower()))
assert visible==expected_words,(len(visible),len(expected_words))
sub=W/'captions.ass';sub.write_text(header)
output=ROOT/'published/jori-flimm-2026-11-02-e012-v1.mp4';output.parent.mkdir(exist_ok=True)
cmd('ffmpeg','-nostdin','-y','-loglevel','error','-i',video,'-i',audio,'-filter_complex',f'[0:v]ass={sub}[v]','-map','[v]','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',output)
rendered=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(output)],text=True).strip())
assert output.stat().st_size>1_000_000 and abs(rendered-D)<.25
print(f'JORI_EPISODE_RENDER_OK episode=12 duration={rendered} bytes={output.stat().st_size} tiktok_safe_right=540')
