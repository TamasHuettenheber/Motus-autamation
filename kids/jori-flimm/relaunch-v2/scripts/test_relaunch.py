"""Contract tests for relaunch story and fail-closed video release."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from generate_episode import validate_candidate, assemble_narration
from quality_gate import validate_quality,REQUIRED

def story():
    return {
        "title":"Das flackernde Fenster von Flockenfels",
        "hook":"Plötzlich flackerte mitten im Schnee ein Licht, obwohl hier kein Haus stand!",
        "story":(
            "Jori blieb mitten auf der Gasse stehen. Vor ihm glomm ein kleines goldenes "
            "Licht zwischen den Steinen. Doch als er näher kam, hüpfte es plötzlich "
            "hinter einen Schneehaufen. Ein winziges Laternenwesen mit einer Mütze "
            "tauchte auf: Flimm! Jori fragte vorsichtig, ob er helfen dürfe. "
            "Flimm zeigte ihm drei Wegweiser: der linke trug einen Mond, "
            "der mittlere eine goldene Sonne und der rechte einen Stern. "
            "Ein Schildchen verriet: Nur das Zeichen, das auch nachts leuchtet, "
            "zeigt den Weg zur verlorenen Laterne. Jori nickte Flimm ermutigend zu."
        ),
        "riddle":{"type":"logic","question":"Welches der drei Zeichen leuchtet auch nachts am Himmel?",
                  "answer":"Der Stern.","evidence_in_story":"Nur das Zeichen, das auch nachts leuchtet",
                  "pause_seconds":7},
        "after_answer":"Flimm berührte vorsichtig den Wegweiser mit dem Stern. "
                       "Das Licht wurde größer und beide konnten endlich den Weg erkennen.",
        "cliffhanger":"Da klopfte dreimal etwas gegen eine Tür, die vorher gar nicht im Schnee gestanden hatte.",
        "scene_briefs":[
            "Winterliches Flockenfels: Jori schaut erstaunt auf ein flackerndes Licht im Schnee. Rote Strickmütze, blauer Mantel, warmer Fantasielook.",
            "Erstes Treffen: Flimm, ein kleines goldbraunes Laternenwesen mit Sternenbauch, schaut vorsichtig aus dem Schnee hervor, Jori kniet neben ihm.",
            "Drei deutlich sichtbare Wegweiser in EINEM Bild: Mond links, Sonne in der Mitte, Stern rechts; beide Hauptfiguren davor, lesbare Symbole.",
            "Die drei Wegweiser mit Mond, Sonne und Stern bleiben sichtbar, Jori und Flimm überlegen, Sternenbauch leuchtet sanft, keine Lösung hervorheben.",
            "Flimm zeigt auf das richtige Sternsymbol am Wegweiser, goldenes Licht führt die zwei Freunde in den Wald, Jori freut sich.",
            "Jori und Flimm sehen staunend eine geheimnisvolle Tür, die mitten auf dem verschneiten Weg erscheint; Neugier und warmer Lichtschein."
        ],
        "critical_visual_objects":["drei Wegweiser","Mond","Sonne","Stern"]
    }

class StoryStructure(unittest.TestCase):
    def test_canonical_good_story(self):
        self.assertTrue(validate_candidate(story(),[],1))
        d=story();n=assemble_narration(d)
        self.assertEqual(n.count("[[PAUSE:7]]"),1)
        self.assertLess(n.index(d["riddle"]["question"]),n.index("[[PAUSE:7]]"))
        self.assertGreater(n.index(d["riddle"]["answer"]),n.index("[[PAUSE:7]]"))
        self.assertTrue(n.endswith(d["cliffhanger"]))
    def test_no_boring_intro(self):
        p=story();p["hook"]="Willkommen, alle Kinder. Wir erzählen euch heute eine schöne Geschichte."
        with self.assertRaisesRegex(ValueError,"greeting"):
            validate_candidate(p,[],1)
    def test_no_missing_clues_in_visual_prompts(self):
        p=story();p["critical_visual_objects"]=["ein roter Drache"]
        with self.assertRaisesRegex(ValueError,"clue"):
            validate_candidate(p,[],1)
    def test_no_duplicate_riddles(self):
        p=story()
        with self.assertRaisesRegex(ValueError,"Riddle reused"):
            validate_candidate(p,[{"episode_number":2,"title":"Anders",
                "hook":"Anders","cliffhanger":"Ganz anders",
                "riddle":{"question":p["riddle"]["question"]}}],3)
    def test_no_same_episode_number(self):
        with self.assertRaisesRegex(ValueError,"reserved"):
            validate_candidate(story(),[{"episode_number":1}],1)
    def test_no_short_story_and_wrong_pause(self):
        p=story();p["story"]="Jori und Flimm sahen was."
        with self.assertRaisesRegex(ValueError,"story length"):
            validate_candidate(p,[],1)
        p=story();p["riddle"]["pause_seconds"]=2
        with self.assertRaisesRegex(ValueError,"seven seconds"):
            validate_candidate(p,[],1)

class VideoReleaseChecks(unittest.TestCase):
    def sample(self):
        p=story()
        p.update({
            "series_version":"relaunch-v2","episode_number":1,
            "approved_for_publish":False,
            "voice":{"provider":"Gemini TTS 3.8","speaker_id":"Sulafat"},
            "narration":assemble_narration(p)
        })
        return p
    def report(self,p):
        h=hashlib.sha256(json.dumps(p,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        return {
            "series_version":"relaunch-v2","episode_number":1,
            "source_draft_sha256":h,
            "checks":{x:{"status":"PASS","evidence":f"QA looked at actual output for {x}"}
                     for x in REQUIRED},
            "measured_silent_thinking_pause_seconds":7.03,
            "riddle_caption_held_during_pause":True,
            "spoken_solution_after_pause":True,
            "speech_recognition_method":"local_asr_reviewed",
            "transcription_word_error_rate":0.01,
            "max_subtitle_offset_seconds":0.25,
            "measured_audio_lufs":-13.4,
            "measured_true_peak_dbtp":-1.8,
            "device_test":"iPhone MP4 audio confirmed",
            "scene_visual_review":[{"scene":i,"matched":True,
                "proof":f"Scene {i} actual image and all objects reviewed"} for i in range(1,7)],
            "confirmed_visible_riddle_objects":p["critical_visual_objects"][:],
            "final_reviewer":{"method":"watched_and_listened_full_render","identity":"Quality Controller"},
            "final_video_sha256":"a"*64
        }
    def test_missing_evidence_blocks(self):
        p=self.sample();r=self.report(p)
        del r["checks"]["subtitle_sync"]
        with self.assertRaisesRegex(ValueError,"subtitle_sync"):
            validate_quality(p,r)
    def test_missing_three_symbols_blocks(self):
        p=self.sample();r=self.report(p)
        r["confirmed_visible_riddle_objects"]=["drei Wegweiser","Mond","Sonne"]
        with self.assertRaisesRegex(ValueError,"visual clues"):
            validate_quality(p,r)
    def test_timing_drift_blocks(self):
        p=self.sample();r=self.report(p)
        r["max_subtitle_offset_seconds"]=1.4
        with self.assertRaisesRegex(ValueError,"Subtitle"):
            validate_quality(p,r)
    def test_wrong_voice_blocks(self):
        p=self.sample();r=self.report(p)
        p["voice"]["speaker_id"]="Victoria"
        r["source_draft_sha256"]=hashlib.sha256(json.dumps(p,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        with self.assertRaisesRegex(ValueError,"Sulafat"):
            validate_quality(p,r)
    def test_wrong_series_blocks(self):
        p=self.sample();r=self.report(p)
        p["series_version"]="v1"
        with self.assertRaisesRegex(ValueError,"Old series"):
            validate_quality(p,r)
    def test_no_actual_phone_test_blocks(self):
        p=self.sample();r=self.report(p);r["device_test"]="assumed OK"
        with self.assertRaisesRegex(ValueError,"smartphone"):
            validate_quality(p,r)

if __name__=="__main__":
    unittest.main()
