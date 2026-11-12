"""Offline tests for illustration reuse preview packaging, with NO publishing."""
import json
import tempfile
import unittest
from pathlib import Path

from build_storyboard import BASE, WIDTH, HEIGHT, build, validate_draft
from PIL import Image

FIXTURE = BASE / "fixtures" / "e002-draft-2026-10-22.json"


class StoryboardPreviewTests(unittest.TestCase):
    def test_preview_is_six_valid_images_and_not_approved(self):
        with tempfile.TemporaryDirectory() as t:
            result = build(FIXTURE, Path(t))
            manifest = json.loads((result / "preview-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "PREVIEW_ONLY")
            self.assertIs(manifest["approved_for_publish"], False)
            self.assertIs(manifest["scheduled_for_tiktok"], False)
            self.assertIs(manifest["new_unique_scene_illustrations"], False)
            self.assertEqual(len(manifest["scenes"]), 6)
            self.assertEqual(len(set(s["source_art"] for s in manifest["scenes"])), 6)
            for s in manifest["scenes"]:
                self.assertIs(s["art_alignment_confirmed"], False)
                with Image.open(result / s["file"]) as img:
                    self.assertEqual(img.size, (WIDTH, HEIGHT))
                    self.assertEqual(img.format, "JPEG")

    def test_approved_draft_is_refused(self):
        draft = json.loads(FIXTURE.read_text(encoding="utf-8"))
        draft["approved_for_publish"] = True
        with self.assertRaisesRegex(ValueError, "unpublished"):
            validate_draft(draft)

    def test_unknown_status_is_refused(self):
        draft = json.loads(FIXTURE.read_text(encoding="utf-8"))
        draft["status"] = "published"
        with self.assertRaisesRegex(ValueError, "status"):
            validate_draft(draft)

    def test_second_preview_same_episode_is_refused(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            build(FIXTURE, root)
            with self.assertRaises(FileExistsError):
                build(FIXTURE, root)


if __name__ == "__main__":
    unittest.main()
