# Jori & Flimm – Kids Short-Story Pipeline

Status: isolated build on `feature/jori-flimm-kids-pipeline`. This work does not change `main` or the live Motus workflow.

## Content boundary

The book `Die 24 verschwundenen Weihnachtslichter` is canon for character and world details only. Its 24 missions, 48 tasks, solutions, light-letter sequence, and final message stay exclusive to the book. Videos use new side stories and riddles.

## Free renderer

The renderer turns 5–10 still images into a 1080×1920 H.264 slideshow with slow alternating zoom and pan, narration, safe-zone subtitles without an opaque box, and technical QC. It accepts supplied HTTPS audio or generates German narration with Piper's `de_DE-mls-medium` voice and female speaker ID 86. The model is medium quality; the story renderer uses a slightly quicker pace, deliberate sentence pauses, and gentle warmth EQ. The Multilingual LibriSpeech dataset is CC BY 4.0, so published use must include attribution to the dataset/model source. Scene timing scales to narration; clips target 60 seconds or more and reject long silent gaps. Rendered MP4 files are retained as seven-day Actions artifacts; successful episode JSON and continuity state are committed on this feature branch.

Caption timing is estimated from word counts. Captions use white bold text with a dark outline and shadow instead of a black panel. Timing and mobile safe-area placement still need a final viewing review.

## Files

- `series-bible.md`: canon and episode rules
- `pipeline-spec.md`: workflow, payload, and rollout details
- `episode-state.schema.json`: payload contract
- `state/series-state.json`: current character and world continuity
- `state/episode-ledger.json`: recent titles, hooks, riddles, and visual asset usage
- `test-payload-episode-000.json`: first-meeting side-story payload with six original AI-generated illustrations
- `assets/e000/`: six 720×1280 JPEG scene illustrations used by Episode 000

## Safe test procedure

A narrowly filtered `push` trigger is configured for changes to the Episode 000 test payload on `feature/jori-flimm-kids-pipeline`. It loads that fixture directly, renders generated German TTS with the MLS medium female-speaker profile, original AI-generated Jori & Flimm illustrations, slow zoom/pan, safe-zone captions, and technical QC. GitHub Actions run #8 succeeded: 65.6 seconds, 1080×1920, H.264/AAC. The MP4 is available as a seven-day artifact. The new voice is a free candidate for the user's listen-through; pronunciation and story quality still need a human review before public use.

The daily handoff remains manual. GitHub only exposes `workflow_dispatch` after its workflow exists on the default branch, so it is not enabled for the feature branch yet.

## Publishing

No publishing workflow or second social account is connected. Publishing stays out of scope until the user explicitly authorizes a second channel/login and a private or draft post test.
