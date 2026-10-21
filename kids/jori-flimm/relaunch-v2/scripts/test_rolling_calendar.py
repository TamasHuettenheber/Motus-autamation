"""Europe/Berlin one-episode-per-day publication and preproduction guard tests."""
import copy
import datetime as dt
import json
import unittest
from pathlib import Path

from rolling_calendar import ROOT, next_episode_dates, production_for, check_plan

class FiveDayPublishing(unittest.TestCase):
    def setUp(self):
        self.plans=next_episode_dates(12)
        self.posts=json.loads((ROOT/"buffer_folgen_001_005_entwuerfe.json").read_text(encoding="utf-8"))
    def test_five_days_exactly_once_14_local(self):
        self.assertEqual([p["date"] for p in self.plans[:5]],[
            "2026-10-23","2026-10-24","2026-10-25","2026-10-26","2026-10-27"])
        self.assertTrue(all(p["local"].startswith(p["date"]+"T14:00:00") for p in self.plans))
        self.assertTrue(check_plan(self.plans,self.posts))
    def test_dst_change_october_25(self):
        self.assertEqual(self.plans[0]["dueAt"],"2026-10-23T12:00:00Z")
        self.assertEqual(self.plans[1]["dueAt"],"2026-10-24T12:00:00Z")
        self.assertEqual(self.plans[2]["dueAt"],"2026-10-25T13:00:00Z")
        self.assertEqual(self.plans[4]["dueAt"],"2026-10-27T13:00:00Z")
    def test_next_episode_six_follows_not_all_at_once(self):
        self.assertEqual(self.plans[5]["date"],"2026-10-28")
        self.assertEqual(self.plans[5]["local"],"2026-10-28T14:00:00+01:00")
    def test_episode_six_produced_three_days_early(self):
        p=production_for(self.plans[5])
        self.assertEqual(p["first_draft_at"],"2026-10-25T20:00:00+01:00")
        self.assertEqual(p["release_deadline"],"2026-10-27T19:00:00+01:00")
    def test_false_scheduled_status_never_confused_for_scheduled(self):
        self.assertTrue(all(p["scheduled_in_buffer"] is False for p in self.posts["posts"]))
    def test_misplaced_dailies_blocked(self):
        data=copy.deepcopy(self.posts)
        data["posts"][1]["scheduled_for_utc"]="2026-10-23T12:00:00Z"
        with self.assertRaisesRegex(ValueError,"schedule"):
            check_plan(self.plans,data)
    def test_lie_about_scheduling_blocked(self):
        data=copy.deepcopy(self.posts)
        data["posts"][0]["scheduled_in_buffer"]=True
        with self.assertRaisesRegex(ValueError,"Buffer post ID"):
            check_plan(self.plans,data)
    def test_lie_about_publication_blocked(self):
        data=copy.deepcopy(self.posts)
        data["posts"][0]["published_on_tiktok"]=True
        with self.assertRaisesRegex(ValueError,"TikTok link"):
            check_plan(self.plans,data)
if __name__=="__main__":unittest.main()
