# Pipeline Specification – Jori & Flimm

## Isolation

The implementation is restricted to `feature/jori-flimm-kids-pipeline`. The manual handoff and renderer reject any other ref. A separate push trigger is configured only for changes to the Episode 000 fixture on this feature branch; it enables a technical render without merging. Actions run #11 completed successfully with the same original illustrations, story text, zoom/pan, and subtitles; only the narration source/settings changed. It uses the online Microsoft Edge Read Aloud service through the `edge-tts` client with German female voice `de-DE-KatjaNeural`, rate -5%, and pitch -1Hz. QC passed at 1080×1920 H.264/AAC. The seven-day MP4 is ready for the user's listen-through. The test needs internet and no paid TTS account or API key; the unofficial client/service can change or stop working, so this remains a free audition path rather than a guaranteed production service. No publishing workflow, issue-open trigger, or change to the Motus master workflow is included.

The daily handoff can later receive a fifth content package from the shared 22:37 producer, but that integration must be implemented separately after the isolated renderer is proven.

## Payload and renderer

A `[JORI-FLIMM-DAY]` issue body contains one JSON object validated against `episode-state.schema.json`. The renderer requires a valid date, non-negative episode number, title, hook, narration, riddle, 5–10 HTTPS still-image URLs, 4–20 seconds per scene, and positive QC gates. An audio URL is optional.

If `audio_url` is supplied, the renderer downloads it. Otherwise the `edge-tts` client requests a German neural voice from Microsoft Edge Read Aloud; the Episode 000 fixture selects female `de-DE-KatjaNeural` with a slightly slower rate and lower pitch. The test needs internet and no paid TTS account or API key. The client uses an online service without a production guarantee; its availability or behavior may change. FFmpeg creates vertical H.264/AAC output at 1080×1920 and 30 fps, applies alternating slow zoom and pan to still images, and burns word-timed, bottom-centered white subtitles with a dark outline and shadow, with no opaque black background. Scene durations scale to the voice track with a 45-second minimum and a short, calm visual tail after narration. The MP4 is uploaded as a seven-day Actions artifact instead of being committed to Git.

Caption timing is estimated by word count, not forced alignment. Technical QC checks output dimensions, codecs, audio presence, duration, and the narration/visual timeline. A person must still review pronunciation, caption readability, character visuals, canon fit, and story quality.

## State and continuity

Before an episode, the producer should read:
- `state/series-state.json` for relationship stage, known facts, active threads, and the book boundary
- the most recent 30 episode titles/hooks and 50 riddles in `state/episode-ledger.json`

After successful QC, the renderer stores the episode payload, updates the ledger with its title, hook, riddle, and scene assets, and applies an optional `continuity_after` handoff to series state. Episode numbers are replaced idempotently on reruns. Exact title, hook, and riddle-question duplicates are rejected against the ledger.

## Episode 000 technical fixture

`test-payload-episode-000.json` is a new side story about Jori and Flimm meeting at an old bridge. It does not retell a book mission. It uses six original AI-generated story illustrations and generated German TTS for an end-to-end illustrated preview.

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
