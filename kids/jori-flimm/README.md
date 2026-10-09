# Jori & Flimm – Kids Short-Story Pipeline

Status: isolated build on `feature/jori-flimm-kids-pipeline`. This work does not change `main` or the live Motus workflow.

## Content boundary

The book `Die 24 verschwundenen Weihnachtslichter` is canon for character and world details only. Its 24 missions, 48 tasks, solutions, light-letter sequence, and final message stay exclusive to the book. Videos use new side stories and riddles.

## Free renderer

The renderer turns 5–10 still images into a 1080×1920 H.264 slideshow with slow alternating zoom and pan, narration, safe-zone subtitles without an opaque box, and technical QC. It accepts supplied HTTPS audio or generates narration using the German female voice Victoria (`df_victoria`) from the Apache-2.0 `kikiri-tts/kikiri-german-victoria` model through the Hugging Face CPU demo. Episode 000 begins with: “Willkommen bei Jori und Flimm. Heute beginnt unsere erste gemeinsame Geschichte.” The renderer splits narration into chunks below the demo’s current 300-character guest limit and adds short pauses between them. No TTS API key or paid account is required. The public demo can change or become unavailable, and its logs include generated text; only send story text intended for publication. The model weights are Apache-2.0, but the hosted demo is a separate service and has no production availability guarantee. Scene timing scales to narration; clips target at least 45 seconds and keep a short, calm visual tail after the narration. Rendered MP4 files are retained as seven-day Actions artifacts; successful episode JSON and continuity state are committed on this feature branch.

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

A narrowly filtered `push` trigger is configured for changes to the Episode 000 test payload on `feature/jori-flimm-kids-pipeline`. It loads that fixture directly, renders the German Victoria narration through the Hugging Face CPU demo, the original AI-generated Jori & Flimm illustrations, slow zoom/pan, safe-zone captions, and technical QC. The ending now includes Flimm and Jori's reaction, their plan to follow the light tomorrow, and a final quiet beat with a gentle fade. GitHub Actions run #14 succeeded: 77.2 seconds, 1080×1920 H.264/AAC. The MP4 is available as a seven-day artifact. This no-paid-account test still needs a human listen-through for pronunciation, warmth, and story quality before public use.

The daily handoff remains manual. GitHub only exposes `workflow_dispatch` after its workflow exists on the default branch, so it is not enabled for the feature branch yet.

## Publishing

No publishing workflow or second social account is connected. Publishing stays out of scope until the user explicitly authorizes a second channel/login and a private or draft post test.
