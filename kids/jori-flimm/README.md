# Jori & Flimm – Kids Short-Story Pipeline

Status: isolated build on `feature/jori-flimm-kids-pipeline`. This work does not change `main` or the live Motus workflow.

## Content boundary

The book `Die 24 verschwundenen Weihnachtslichter` is canon for character and world details only. Its 24 missions, 48 tasks, solutions, light-letter sequence, and final message stay exclusive to the book. Videos use new side stories and riddles.

## Free renderer

The renderer turns 5–10 still images into a 1080×1920 H.264 slideshow with slow alternating zoom and pan, narration, safe-zone subtitles without an opaque box, and technical QC. It accepts supplied HTTPS audio or generates narration using the online Microsoft Edge Read Aloud voice service through the `edge-tts` client. Episode 000 tests the German female voice `de-DE-KatjaNeural` at a slightly slower pace and lower pitch. This test needs internet access and uses no paid TTS account or API key; the unofficial client/service can change or stop working, so it is a free audition path rather than a guaranteed production service. Scene timing scales to narration; clips target 60 seconds or more and reject long silent gaps. Rendered MP4 files are retained as seven-day Actions artifacts; successful episode JSON and continuity state are committed on this feature branch.

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

A narrowly filtered `push` trigger is configured for changes to the Episode 000 test payload on `feature/jori-flimm-kids-pipeline`. It loads that fixture directly, renders German narration with `de-DE-KatjaNeural` through Edge Read Aloud, the original AI-generated Jori & Flimm illustrations, slow zoom/pan, safe-zone captions, and technical QC. GitHub Actions run #11 succeeded: 1080×1920 H.264/AAC. The MP4 is available as a seven-day artifact. This no-paid-account test still needs a human listen-through for pronunciation, warmth, and story quality before public use.

The daily handoff remains manual. GitHub only exposes `workflow_dispatch` after its workflow exists on the default branch, so it is not enabled for the feature branch yet.

## Publishing

No publishing workflow or second social account is connected. Publishing stays out of scope until the user explicitly authorizes a second channel/login and a private or draft post test.
