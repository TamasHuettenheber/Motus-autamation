# Jori & Flimm – Kids Short-Story Pipeline

Status: isolated build on `feature/jori-flimm-kids-pipeline`. This work does not change `main` or the live Motus workflow.

## Content boundary

The book `Die 24 verschwundenen Weihnachtslichter` is canon for character and world details only. Its 24 missions, 48 tasks, solutions, light-letter sequence, and final message stay exclusive to the book. Videos use new side stories and riddles.

## Free renderer

The renderer turns 5–10 still images into a 1080×1920 H.264 slideshow with slow alternating zoom and pan, narration, safe-zone subtitles, and technical QC. It accepts a supplied HTTPS audio file or creates German narration with free `espeak-ng` TTS. Scene timing scales to the narration; clips target 60 seconds or more and reject long silent gaps. Rendered MP4 files are retained as a seven-day Actions artifact; successful episode JSON and continuity state are committed on this feature branch.

Caption timing is estimated from word counts. It is suitable for a technical preview, not a final accessibility review.

## Files

- `series-bible.md`: canon and episode rules
- `pipeline-spec.md`: workflow, payload, and rollout details
- `episode-state.schema.json`: payload contract
- `state/series-state.json`: current character and world continuity
- `state/episode-ledger.json`: recent titles, hooks, riddles, and visual asset usage
- `test-payload-episode-000.json`: first-meeting technical test story

## Safe test procedure

A narrowly filtered `push` trigger is configured for changes to the Episode 000 test payload on `feature/jori-flimm-kids-pipeline`. It loads that fixture directly, renders with generated TTS and free placeholder stills, uploads the MP4 for seven days, and updates only the kids state files on the feature branch. This path is intended to permit an Actions render without merging to `main`. No run or check appeared in GitHub after the fixture update, so remote render completion is still unverified.

The daily handoff remains manual. GitHub only exposes `workflow_dispatch` after its workflow exists on the default branch, so it is not enabled for the feature branch yet.

## Publishing

No publishing workflow or second social account is connected. Publishing stays out of scope until the user explicitly authorizes a second channel/login and a private or draft post test.
