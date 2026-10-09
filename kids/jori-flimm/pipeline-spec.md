# Pipeline Specification – Jori & Flimm

## Isolation

The implementation is restricted to `feature/jori-flimm-kids-pipeline`. The manual handoff and renderer reject any other ref. The push trigger renders the Episode 000 fixture or one changed episode JSON on this feature branch; it remains isolated and never merges or publishes. Episode 000 now opens with “Willkommen bei Jori und Flimm! Heute beginnt unsere erste gemeinsame Geschichte.” and uses the German female Victoria voice (`df_victoria`) from the Apache-2.0 `kikiri-tts/kikiri-german-victoria` model through the Hugging Face CPU demo. The workflow splits text into chunks below the demo’s current 300-character guest cap and joins them with short pauses. This requires no paid TTS account or API key, but sends the story text to a public demo that logs submitted text; use only publication-ready story text. The demo may change or become unavailable, so it is not a production guarantee. The 84-second feature-branch render passed technical QC; human review is pending. No publishing workflow, issue-open trigger, or change to the Motus master workflow is included.

The daily handoff can later receive a fifth content package from the shared 22:37 producer, but that integration must be implemented separately after the isolated renderer is proven.

## Payload and renderer

A `[JORI-FLIMM-DAY]` issue body contains one JSON object validated against `episode-state.schema.json`. The renderer requires a valid date, non-negative episode number, title, hook, narration, riddle, 5–10 HTTPS still-image URLs, 4–20 seconds per scene, and positive QC gates. An audio URL is optional.

If `audio_url` is supplied, the renderer downloads it. Otherwise, `scripts/generate_voice.py` calls the public Hugging Face Space `nam194/KokoroTTS-HF-CPU` using the Apache-2.0 German Victoria voice (`df_victoria`). Text is split into at most 280-character requests (the Space currently truncates anonymous requests at 300 characters); short silences preserve pauses between chunks. An explicit narration marker such as `[[PAUSE:7]]` inserts an exact 5–10 second thinking pause into the audio and holds the final riddle caption until the answer. No paid TTS account or API key is required. The Space logs generated text and may change or become unavailable, so this path is for publication-ready story text and is not a guaranteed service. FFmpeg creates vertical H.264/AAC output at 1080×1920 and 30 fps, applies alternating slow zoom and pan to still images, and burns word-timed, bottom-centered white subtitles with a dark outline and shadow, with no opaque black background. Scene durations scale to the voice track with a 45-second minimum, 2.2-second visual tail, and a gentle 1.2-second fade. The MP4 is uploaded as a seven-day Actions artifact instead of being committed to Git.

Captions are timed within generated speech chunks by their measured audio lengths, not forced alignment; marked thinking silences hold the riddle caption until speech resumes. Technical QC checks output dimensions, codecs, audio presence, duration, and the narration/visual timeline. A person must still review pronunciation, caption readability, character visuals, canon fit, and story quality.

## State and continuity

Before an episode, the producer should read:
- `state/series-state.json` for relationship stage, known facts, active threads, and the book boundary
- the most recent 30 episode titles/hooks and 50 riddles in `state/episode-ledger.json`

After successful QC, the renderer stores the episode payload, updates the ledger with its title, hook, riddle, and scene assets, and applies an optional `continuity_after` handoff to series state. Episode numbers are replaced idempotently on reruns. Exact title, hook, and riddle-question duplicates are rejected against the ledger.

## Episode 000 technical fixture

`test-payload-episode-000.json` is a new side story about Jori and Flimm meeting at an old bridge. It does not retell a book mission. It uses six original AI-generated story illustrations and generated German TTS for an end-to-end illustrated preview.

A feature-branch push trigger accepts this fixture or one episode payload JSON. It uploads the result as an Actions artifact and commits state/episode metadata only on the feature branch. It does not publish.

## Publishing and rollout

A second-channel publisher is deliberately absent. The required later checkpoint is user connection/authorization for that channel, followed by a private/unlisted or draft post test. Do not merge to `main`, modify live Motus, connect another channel, or publish without the user's explicit approval.

Rollout order:
1. validate workflows, permissions, payload/schema, and feature-branch checks;
2. run and review Episode 000 through the isolated push trigger;
3. fix render/QC issues and document the result;
4. request the user's authorization only when a second channel/login is needed;
5. connect and test publishing privately;
6. merge and add the shared-trigger integration only after explicit approval.
