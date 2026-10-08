# Jori & Flimm – Kids Short-Story Pipeline

Status: isolated build on `feature/jori-flimm-kids-pipeline`. This work does not change `main` or the live Motus workflow.

## Content boundary

The book `Die 24 verschwundenen Weihnachtslichter` is canon for character and world details only. Its 24 missions, 48 tasks, solutions, light-letter sequence, and final message stay exclusive to the book. Videos use new side stories and riddles.

## Free renderer

The renderer turns 5–10 still images into a 1080×1920 H.264 slideshow with slow alternating zoom and pan, narration, safe-zone subtitles, and QC. It accepts a supplied HTTPS audio file or creates German narration with free `espeak-ng` TTS. Rendered MP4 files are retained as a short-lived Actions artifact; successful episode JSON and continuity state are committed on this feature branch.

The initial caption timing is estimated from narration word counts. It is suitable for a technical preview, not a final accessibility review.

## Files

- `series-bible.md`: canon and episode rules
- `pipeline-spec.md`: workflow, payload, and rollout details
- `episode-state.schema.json`: payload contract
- `state/series-state.json`: current character and world continuity
- `state/episode-ledger.json`: recent titles, hooks, riddles, and visual asset usage
- `test-payload-episode-000.json`: first-meeting test story

## Safe test procedure

1. Create a GitHub issue titled `[JORI-FLIMM-DAY] Episode 000 test` and paste the test JSON as the complete issue body.
2. Dispatch `Jori & Flimm Daily Handoff` on `feature/jori-flimm-kids-pipeline` with the issue number and the same target ref.
3. Download the `jori-flimm-2026-10-08-e000` artifact from the renderer run and review narration, captions, character visuals, and QC.
4. Confirm the state files and episode JSON were committed on the feature branch.

GitHub requires a `workflow_dispatch` workflow to exist on the repository's default branch before it can be manually dispatched. The feature-only workflow is therefore prepared but has not been run from GitHub; do not merge it merely to enable a test.

## Publishing

No publishing workflow or second social account is connected. Publishing stays out of scope until the user explicitly authorizes a second channel/login and a private or draft post test.
