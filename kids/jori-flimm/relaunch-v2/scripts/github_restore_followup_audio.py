#!/usr/bin/env python3
"""Recover existing Gemini Sulafat episode audio from GitHub Actions artifact without another TTS call."""
import argparse,os,json,urllib.request,zipfile,io,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--episode",type=int,choices=[3,5],required=True);a=p.parse_args()
artifact={3:12387593363,5:12388237545}[a.episode]
token=os.environ["GH_TOKEN"];repo=os.environ["GITHUB_REPOSITORY"]
url=f"https://api.github.com/repos/{repo}/actions/artifacts/{artifact}/zip"
req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json"})
with urllib.request.urlopen(req,timeout=90) as r:raw=r.read()
z=zipfile.ZipFile(io.BytesIO(raw))
w=Path(f"work/episode_{a.episode:03d}");w.mkdir(parents=True,exist_ok=True)
wav=f"folge_{a.episode:03d}.wav";timeline=f"folge_{a.episode:03d}_timeline.json"
(w/"narration_source.wav").write_bytes(z.read(wav))
(w/"voice-timeline.json").write_bytes(z.read(timeline))
data=json.loads((w/"voice-timeline.json").read_text())
assert len(data["items"])==3 and data["items"][1]["kind"]=="pause" and abs(data["items"][1]["duration"]-7)<.12
assert "sagte er" not in " ".join(x.get("text","") for x in data["items"])
print("JORI_EXISTING_SULAFAT_RESTORED",a.episode,data["duration"])
