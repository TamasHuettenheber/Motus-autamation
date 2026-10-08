# Pipeline Specification – Jori & Flimm

## Isolation

The implementation is restricted to `feature/jori-flimm-kids-pipeline`. The manual handoff and renderer reject any other ref. A separate push trigger is configured only for changes to the Episode 000 fixture on this feature branch; it enables a technical render without merging. Actions run #3 completed with technical QC passing at 70.8 seconds, 1080×1920, H.264/AAC. Its placeholder-card visuals validate layout only; character artwork, voice quality, and story fit still need human review. A fourth run is verifying the continuity merge fix. No publishing workflow, issue-open trigger, or change to the Motus master workflow is included.

The daily handoff can later receive a fifth content package from the shared 22:37 producer, but that integration must be implemented separately after the isolated renderer is proven.

## Payload and renderer

A `[JORI-FLIMM-DAY]` issue body contains one JSON object validated against `episode-state.schema.json`. The renderer requires a valid date, non-negative episode number, title, hook, narration, riddle, 5–10 HTTPS still-image URLs, 4–20 seconds per scene, and positive QC gates. An audio URL is optional.

If `audio_url` is supplied, the renderer downloads it. Otherwise the free `espeak-ng` German voice reads the narration. FFmpeg creates vertical H.264/AAC output at 1080×1920 and 30 fps, applies alternating slow zoom and pan to still images, and burns word-timed subtitles in a safe area. Scene durations scale to the voice track to target at least 60 seconds while keeping the visual ending just after narration. The MP4 is uploaded as a seven-day Actions artifact instead of being committed to Git.

Caption timing is estimated by word count, not forced alignment. Technical QC checks output dimensions, codecs, audio presence, duration, and the narration/visual timeline. A person must still review pronunciation, caption readability, character visuals, canon fit, and story quality.

## State and continuity

Before an episode, the producer should read:
- `state/series-state.json` for relationship stage, known facts, active threads, and the book boundary
- the most recent 30 episode titles/hooks and 50 riddles in `state/episode-ledger.json`

After successful QC, the renderer stores the episode payload, updates the ledger with its title, hook, riddle, and scene assets, and applies an optional `continuity_after` handoff to series state. Episode numbers are replaced idempotently on reruns. Exact title, hook, and riddle-question duplicates are rejected against the ledger.

## Episode 000 technical fixture

`test-payload-episode-000.json` is a new side story about Jori and Flimm meeting at an old bridge. It does not retell a book mission. It uses free placeholder stills and generated German TTS for an end-to-end technical preview.

A feature-branch push trigger is configured only for changes to this one test file. It uploads the result as an Actions artifact and commits state/episode metadata only on the feature branch. It does not publish.

## Publishing and rollout

A second-channel publisher is deliberately absent. The required later checkpoint is user connection/authorization for that channel, followed by a private/unlisted or draft post test. Do not merge to `main`, modify live Motus, connect another channel, or publish without the user's explicit approval.

Rollout order:
1. validate workflows, permissions, payload/schema, and feature-branch checks;
2. run and review Episode 000 through the isolated push trigger;
3. fix render/QC issues and document the result;
4. request the user's authorization only when a second channel/login is needed;
5. connect and test publishing privately;
6. merge and add the shared-trigger integration only after explicit approval.
