"""Test automatic NON-PUBLISHING renderer-payload compilation from six preview images."""
import json
import tempfile
import unittest
from pathlib import Path

from build_storyboard import BASE, build
from compile_preview_episode import compile_preview

FIXTURE=BASE / "fixtures" / "e002-draft-2026-10-22.json"

class CompilePreviewEpisodeTests(unittest.TestCase):
    def test_six_scenes_never_authorize_publish(self):
        with tempfile.TemporaryDirectory() as d:
            folder=build(FIXTURE,Path(d))
            payload=compile_preview(FIXTURE,folder)
            self.assertTrue(payload["preview_only"])
            self.assertEqual(payload["publish_time"],"14:00")
            self.assertEqual(payload["voice"]["speaker_id"],"kerstin")
            self.assertTrue(all(v is False for v in payload["qc"].values()))
            self.assertEqual(len(payload["scenes"]),6)
            self.assertEqual(len(set(s["image_url"] for s in payload["scenes"])),6)

    def test_cannot_compile_approved_or_mismatched_artwork(self):
        with tempfile.TemporaryDirectory() as d:
            folder=build(FIXTURE,Path(d))
            original=json.loads((folder/"preview-manifest.json").read_text(encoding="utf-8"))
            original["approved_for_publish"]=True
            (folder/"preview-manifest.json").write_text(json.dumps(original),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"approved_for_publish"):
                compile_preview(FIXTURE,folder)


if __name__=="__main__":
    unittest.main()
