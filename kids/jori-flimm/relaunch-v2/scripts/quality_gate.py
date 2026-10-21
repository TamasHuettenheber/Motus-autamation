#!/usr/bin/env python3
"""Fail-closed post-render QC for EVERY Jori & Flimm relaunch episode.

Never sets PASS itself. Pass evidence must come from independent checks
(including actual listen/view review of scene-specific images and speech).
Returns nonzero on absent/incomplete evidence. This is a release gate, not
a claim that audio alignment or image checking is already automated.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REQUIRED={
    "story_structure","continuity","original_riddle",
    "speech_transcript","subtitle_sync","visible_riddle_clues",
    "scene_visual_match","character_consistency","sulafat_voice",
    "audio_loudness","mobile_playback","video_integrity",
    "genuine_cliffhanger","human_final_review"
}

def validate_quality(story,report,video=None):
    if story.get("series_version")!="relaunch-v2" or story.get("episode_number",0)<1:
        raise ValueError("Old series episode refused: restart from episode 001")
    if story.get("approved_for_publish") is True:
        raise ValueError("Draft already claims release before QC")
    if report.get("series_version")!="relaunch-v2":
        raise ValueError("QC series identity mismatch")
    if int(report.get("episode_number",-1))!=int(story["episode_number"]):
        raise ValueError("QC episode mismatch")
    if report.get("source_draft_sha256")!=hashlib.sha256(
          json.dumps(story,sort_keys=True,ensure_ascii=False).encode()).hexdigest():
        raise ValueError("Quality report is stale for this exact draft")
    items=report.get("checks") or {}
    for key in sorted(REQUIRED):
        item=items.get(key)
        if not isinstance(item,dict) or item.get("status")!="PASS" or len(str(item.get("evidence","")).strip())<15:
            raise ValueError(f"Missing real quality evidence: {key}")
    voice=story.get("voice") or {}
    if voice.get("speaker_id")!="Sulafat" or voice.get("provider")!="Gemini TTS 3.8":
        raise ValueError("Narrator must be Sulafat")
    if story.get("riddle",{}).get("pause_seconds")!=7 or story.get("narration","").count("[[PAUSE:7]]")!=1:
        raise ValueError("Seven-second thinking pause missing")
    if not 6.7 <= float(report.get("measured_silent_thinking_pause_seconds",-1)) <= 7.3:
        raise ValueError("Measured THINKING pause must last seven seconds")
    if report.get("riddle_caption_held_during_pause") is not True:
        raise ValueError("Riddle caption disappeared during pause")
    if report.get("spoken_solution_after_pause") is not True:
        raise ValueError("Answer was not after the actual pause")
    if report.get("speech_recognition_method") not in {"reviewed_transcript","local_asr_reviewed"}:
        raise ValueError("Actual speech recognition / listen review not documented")
    if float(report.get("transcription_word_error_rate",1)) > .07:
        raise ValueError("Audio differs from approved script (high WER)")
    if float(report.get("max_subtitle_offset_seconds",999)) > .4:
        raise ValueError("Subtitle display does not match the spoken words")
    if not -15.5 <= float(report.get("measured_audio_lufs",-99)) <= -11:
        raise ValueError("Mobile audio too quiet or too loud")
    if float(report.get("measured_true_peak_dbtp",1)) > -0.9:
        raise ValueError("Peak audio level unsafe")
    if report.get("device_test") not in {"iPhone MP4 audio confirmed","Android MP4 audio confirmed"}:
        raise ValueError("Full video smartphone audio test missing")
    visual=report.get("scene_visual_review")
    if not isinstance(visual,list) or len(visual)!=6 or [x.get("scene") for x in visual]!=list(range(1,7)):
        raise ValueError("Six real image-to-story scene checks needed")
    if any(x.get("matched") is not True or len(str(x.get("proof","")))<15 for x in visual):
        raise ValueError("Visible scene items not confirmed")
    confirmed=set(report.get("confirmed_visible_riddle_objects",[]))
    if not set(story.get("critical_visual_objects",[])).issubset(confirmed):
        raise ValueError("Riddle requires visual clues not verified in actual rendered video")
    reviewer=report.get("final_reviewer") or {}
    if reviewer.get("method")!="watched_and_listened_full_render" or len(str(reviewer.get("identity","")).strip())<3:
        raise ValueError("No final original-MP4 listen/view audit recorded")
    if not re.fullmatch(r"[0-9a-f]{64}",str(report.get("final_video_sha256",""))):
        raise ValueError("Video checksum missing or invalid")
    if video is not None:
        f=Path(video)
        if not f.is_file() or not f.stat().st_size:
            raise ValueError("Final video missing")
        if hashlib.sha256(f.read_bytes()).hexdigest()!=report["final_video_sha256"]:
            raise ValueError("Reported release video bytes do not match actual MP4")
        raw=subprocess.check_output(["ffprobe","-v","error","-show_entries",
            "stream=codec_name,width,height:format=duration","-of","json",str(f)],text=True)
        m=json.loads(raw)
        streams=m.get("streams",[])
        v=next((x for x in streams if x.get("codec_name")=="h264"),None)
        a=next((x for x in streams if x.get("codec_name")=="aac"),None)
        if not v or not a or v.get("height",0)<=v.get("width",0):
            raise ValueError("Vertical H264/AAC file required")
    return True

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--draft",type=Path,required=True)
    parser.add_argument("--report",type=Path,required=True)
    parser.add_argument("--video",type=Path,required=True)
    p=parser.parse_args()
    story=json.loads(p.draft.read_text(encoding="utf-8"))
    review=json.loads(p.report.read_text(encoding="utf-8"))
    validate_quality(story,review,p.video)
    print("FULL_RELEASE_QC_PASSED_EVIDENCE_VERIFIED; publish still requires isolated account")

if __name__=="__main__":
    try:main()
    except (ValueError,TypeError,KeyError,RuntimeError,OSError,subprocess.CalledProcessError) as exc:
        print(f"FULL_RELEASE_QC_BLOCKED: {exc}",file=sys.stderr)
        sys.exit(1)
