"""Regression checks for user's E002 corrections: Flimm, speech level, no hedgehog."""
import json
import unittest
from pathlib import Path
from generate_daily_story import BASE

class Episode002FeedbackTests(unittest.TestCase):
    def test_protagonists_and_no_hedgehog_in_narration(self):
        for path in [
            BASE/"fixtures/e002-draft-2026-10-22.json",
            BASE/"episodes/jori-flimm-2026-10-22-e002.json"
        ]:
            p=json.loads(path.read_text(encoding="utf-8"))
            story=p["narration"].casefold()
            self.assertGreaterEqual(story.count("jori"),4)
            self.assertGreaterEqual(story.count("flimm"),5)
            self.assertNotIn("igel",story)
            self.assertIn("[[pause:7]]",story)
    def test_voice_set_to_offline_german(self):
        p=json.loads((BASE/"episodes/jori-flimm-2026-10-22-e002.json").read_text(encoding="utf-8"))
        voice=p.get("voice",{})
        self.assertEqual(voice.get("provider"),"Piper local TTS")
        self.assertEqual(voice.get("model"),"de_DE-kerstin-low")
        self.assertIs(p.get("preview_only"),True)
        self.assertEqual(p.get("qc",{}),{"book_spoiler_check":False,"continuity_check":False,"duplicate_check":False})

if __name__=="__main__":
    unittest.main()
