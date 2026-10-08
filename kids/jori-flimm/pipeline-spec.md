# Pipeline Specification – Jori & Flimm

## Isolation

This implementation is restricted to `feature/jori-flimm-kids-pipeline`. Both manual handoff and renderer workflows reject any other ref. The daily handoff is manual for now; there is no issue-open trigger, no publishing workflow, and no change to the Motus master workflow or `main`.

The initial architecture can later receive a fifth content package from the shared 22:37 producer, but that integration must be implemented separately after this isolated renderer is proven.

## Payload and renderer

A `[JORI-FLIMM-DAY]` issue body contains one JSON object validated against `episode-state.schema.json`. The renderer requires a valid date, non-negative episode number, title, hook, narration, riddle, 5–10 HTTPS still-image URLs, 4–20 seconds per scene, and positive QC gates. An audio URL is optional.

If `audio_url` is supplied, the renderer downloads it. Otherwise the free `espeak-ng` German voice reads the narration. FFmpeg creates vertical H.264/AAC output at 1080×1920 and 30 fps, applies alternating slow zoom and pan to still images, and burns word-timed subtitles in a safe area. The MP4 is uploaded as a seven-day Actions artifact instead of being committed to Git.

Captions are timed by word count, not forced alignment. QC checks output dimensions, codecs, audio presence, and duration; a person must still review pronunciation, caption readability, image/canon fit, and story quality.

## State and continuity

Before an episode, the producer should read:
- `state/series-state.json` for relationship stage, known facts, active threads, and the book boundary
- the most recent 30 episode titles/hooks and 50 riddles in `state/episode-ledger.json`

After successful QC, the renderer stores the episode payload, updates the ledger with its title, hook, riddle, and scene assets, and applies an optional `continuity_after` handoff to series state. Episode numbers are replaced idempotently on reruns.

## Episode 000 technical fixture

`test-payload-episode-000.json` is a new side story about Jori and Flimm meeting at an old bridge. It does not retell a book mission. It uses freely served placeholder stills and generated German TTS for an end-to-end technical preview.

The dispatch path requires the workflow to be present on GitHub's default branch. Since this project must not merge before approval, the current fixture is prepared and schema-checked but no remote Actions render has been started.

## Publishing and rollout

A second-channel publisher is deliberately absent. The required later checkpoint is user connection/authorization for that channel, followed by a private/unlisted or draft post test. Do not merge to `main`, modify live Motus, connect another channel, or publish without the user's explicit approval.

Rollout order:
1. validate workflows, permissions, payload/schema, and feature-branch checks;
2. run and review Episode 000 on the feature branch when a safe Actions dispatch is available;
3. fix render/QC issues and document the result;
4. request the user's authorization only when a second channel/login is needed;
5. connect and test publishing privately;
6. merge and add the shared-trigger integration only after explicit approval.
