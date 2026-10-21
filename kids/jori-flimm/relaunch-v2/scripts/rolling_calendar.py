#!/usr/bin/env python3
"""One episode per day, 14:00 Europe/Berlin; rolling pipeline with 3-day lead.

This script NEVER publishes and NEVER changes Buffer. Calendar dates are
calculated using IANA timezone (survives the October DST change).
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE=ZoneInfo("Europe/Berlin")
UTC=dt.timezone.utc
ROOT=Path(__file__).resolve().parents[1]
FIRST=dt.date(2026,10,23)
INTERVAL=dt.timedelta(days=1)
INITIAL=5

def publish_at(day):
    return dt.datetime.combine(day,dt.time(hour=14),tzinfo=ZONE)

def next_episode_dates(last=12):
    if not isinstance(last,int) or last<1 or last>10000:
        raise ValueError("Episode range 1..10000")
    return [{
        "episode_number":n,
        "date":(FIRST+dt.timedelta(days=n-1)).isoformat(),
        "local":publish_at(FIRST+dt.timedelta(days=n-1)).isoformat(),
        "dueAt":publish_at(FIRST+dt.timedelta(days=n-1)).astimezone(UTC).isoformat().replace("+00:00","Z"),
        "timezone":"Europe/Berlin"
    } for n in range(1,last+1)]

def production_for(ep):
    day=dt.date.fromisoformat(ep["date"])
    prep=day-dt.timedelta(days=3)
    # Three days lead: every day produce the new episode due in 3 days.
    return {
        "episode_number":ep["episode_number"],
        "first_draft_at":dt.datetime.combine(prep,dt.time(20,0),tzinfo=ZONE).isoformat(),
        "illustration_and_tts_at":dt.datetime.combine(prep,dt.time(20,30),tzinfo=ZONE).isoformat(),
        "full_video_qc_at":dt.datetime.combine(prep,dt.time(21,30),tzinfo=ZONE).isoformat(),
        "release_deadline":dt.datetime.combine(day-dt.timedelta(days=1),dt.time(19,0),tzinfo=ZONE).isoformat(),
        "publish_at":ep["local"],
        "requires_qc_pass":True,
        "release_action":"schedule_in_Buffer_only_after_full_final_QC"
    }

def check_plan(plans,release_data):
    if len(plans)<5 or any(p["episode_number"]!=i+1 for i,p in enumerate(plans)):
        raise ValueError("Episodes must be consecutive beginning at 001")
    for i,p in enumerate(plans):
        expected=FIRST+dt.timedelta(days=i)
        if dt.date.fromisoformat(p["date"])!=expected:
            raise ValueError("Episode date mismatch")
        if p["dueAt"]!=publish_at(expected).astimezone(UTC).isoformat().replace("+00:00","Z"):
            raise ValueError("Wrong UTC / DST conversion")
    posts=release_data.get("posts",[])
    if len(posts)!=5:raise ValueError("Need exactly five initial posts")
    for i,post in enumerate(posts):
        ep=plans[i]
        if post["folge"]!=ep["episode_number"] or post["scheduled_for_utc"]!=ep["dueAt"]:
            raise ValueError("Buffer post schedule contradicts story calendar")
        if post.get("scheduled_in_buffer") is True and (not post.get("buffer_post_id")):
            raise ValueError("Cannot claim scheduled without confirmed Buffer post ID")
        if post.get("published_on_tiktok") is True and (not post.get("public_tiktok_url")):
            raise ValueError("Cannot claim published without real public TikTok link")
    return True

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--episodes",type=int,default=12)
    p.add_argument("--write",default=None)
    a=p.parse_args()
    plans=next_episode_dates(a.episodes)
    data=json.loads((ROOT/"buffer_folgen_001_005_entwuerfe.json").read_text(encoding="utf-8"))
    check_plan(plans,data)
    result={"series":"Jori & Flimm Restart","timezone":"Europe/Berlin","publication_status":"PLAN_ONLY_NOT_SCHEDULED",
      "posting_frequency":"DAILY one episode exactly at 14:00 local time",
      "publication_targets":plans,
      "rolling_production":[production_for(x) for x in plans if x["episode_number"]>=6],
      "buffer_queue_minimum_target":3,
      "overdue_policy":"NO_UNAPPROVED_RELEASE; flag gap for human review instead of duplicate or wrong video",
      "voice":"Sulafat","publishing_only_after_review":True}
    if a.write:
        dest=Path(a.write);dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for x in plans:
        print(f"PLAN_ONLY EP{x['episode_number']:03d} {x['local']} UTC={x['dueAt']}")
    print("RELEASE_PUBLISHING_DISABLED; Schedule is only a checked plan.")

if __name__=="__main__":
    try:main()
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print("RELEASE_CALENDAR_BLOCKED: "+str(exc),file=sys.stderr)
        sys.exit(1)
