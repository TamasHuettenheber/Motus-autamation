#!/usr/bin/env python3
"""Offline tests for the Jori & Flimm fail-closed story draft validator."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_daily_story import validate

def sample():
    question = "Welcher der drei Wege zeigt nach links?"
    answer = "Der Weg mit dem blauen Schild."
    return {
        "title": "Die Spur des blauen Schildes",
        "hook": "Ein verschneiter Abzweig stellt Jori vor ein Rätsel.",
        "narration": (
            "Jori und Flimm liefen durch einen ruhigen verschneiten Garten. "
            "An der Kreuzung entdeckten sie drei Schilder, die ganz unterschiedlich "
            "aussahen. Flimm wackelte neugierig mit seiner warmen kleinen Laterne. "
            "Jori sah erst genau hin und bemerkte an dem ersten Schild einen blauen "
            "Pfeil, an dem zweiten einen roten Kreis und an dem dritten eine gelbe "
            "Sternenspur. Gemeinsam überlegten sie, wie sie den alten Weg finden. "
            + question + " [[PAUSE:7]] " + answer +
            " Flimm hüpfte vor Freude und die beiden gingen gemeinsam weiter."
        ),
        "riddle": {"type": "direction", "question": question, "answer": answer, "pause_seconds": 7},
        "scene_briefs": [
            f"Jori und Flimm am sicheren Schneeweg aus Kameraperspektive Nummer {i}."
            for i in range(6)
        ],
        "continuity_note": "Jori und Flimm kennen jetzt den Weg zum kleinen Garten.",
        "next_cliffhanger": "Hinter einem Tor hören sie ein sanftes Glockenspiel."
    }

class StoryDraftTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate(sample(), [], 2))

    def test_same_title_rejected(self):
        draft = sample()
        old = {"episode_number": 1, "title": draft["title"], "hook": "Andere Hook", "riddle": {"question": "Anderes Rätsel"}}
        with self.assertRaisesRegex(ValueError, "Duplicate title"):
            validate(draft, [old], 2)

    def test_same_riddle_rejected(self):
        draft = sample()
        old = {"episode_number": 1, "title": "Anderer Titel", "hook": "Andere Hook",
               "riddle": {"question": draft["riddle"]["question"]}}
        with self.assertRaisesRegex(ValueError, "Duplicate riddle"):
            validate(draft, [old], 2)

    def test_missing_pause_rejected(self):
        draft = sample()
        draft["narration"] = draft["narration"].replace("[[PAUSE:7]]", "")
        with self.assertRaisesRegex(ValueError, "pause"):
            validate(draft, [], 2)

    def test_answer_before_pause_rejected(self):
        draft = sample()
        draft["narration"] = draft["narration"].replace("Der Weg mit dem blauen Schild.", "Nehmt die linke Spur.")
        with self.assertRaisesRegex(ValueError, "answer"):
            validate(draft, [], 2)

    def test_same_episode_number_rejected(self):
        with self.assertRaisesRegex(ValueError, "number"):
            validate(sample(), [{"episode_number": 2, "title": "Andere Geschichte",
                                 "hook": "Andere Frage", "riddle": {"question": "Unbekannt"}}], 2)

if __name__ == "__main__":
    unittest.main()
