# Pipeline Specification – Jori & Flimm

## Architecture decision
Use the SAME ChatGPT master production trigger as Motus, but NOT the same GitHub render job.

The 22:37 run should eventually create two independent handoffs:
- Motus daily batch: 4 existing slots
- Jori & Flimm daily batch: 1 kids episode

Reason: a failure in the kids pipeline must never block Motus, and a Motus failure must not corrupt the kids series state.

## Proposed repository layout
```
kids/jori-flimm/
  README.md
  series-bible.md
  pipeline-spec.md
  episode-state.schema.json
  state/
    series-state.json
    episode-ledger.json
  assets/
    characters/
    backgrounds/
    scenes/
  output/
    YYYY-MM-DD/
.github/workflows/
  kids-day.yml
  kids-render.yml
  kids-publish.yml
```

## Daily content object
The producer should create one JSON object:

```json
{
  "date": "YYYY-MM-DD",
  "episode_number": 1,
  "title": "...",
  "hook": "...",
  "narration": "...",
  "riddle": {
    "type": "logic",
    "question": "...",
    "answer": "...",
    "pause_seconds": 3
  },
  "scenes": [
    {
      "order": 1,
      "duration_seconds": 10,
      "image_source": "...",
      "caption": "..."
    }
  ],
  "cta": "...",
  "publish_time": "16:00",
  "book_spoiler_check": true,
  "continuity_check": true,
  "duplicate_check": true
}
```

## Render target
- 1080x1920
- H.264
- AAC audio
- 30 fps
- target duration 60–90 seconds
- max 100 seconds for initial testing
- narration must finish before video end
- safe-zone subtitles
- music below narration
- no text hidden by TikTok UI

## Free-first visual method
Phase 1 does NOT require AI video.
Renderer uses still images and applies:
- scale/zoom
- pan
- crossfade
- optional particle/snow overlay
- subtitle timing

A unique still-image generator may be added later, but the renderer itself must work with a reusable asset library so the pipeline has a zero-paid-generation fallback.

## Quality gates
Reject publication when any gate fails:
- missing scene image
- narration shorter/longer than timeline by unsafe margin
- duplicate or near-duplicate riddle
- duplicate title/hook
- book mission leakage
- wrong character names
- wrong aspect ratio
- missing audio
- unreadable captions
- episode state not committed

## State
Before producing an episode, load:
- previous 30 episode titles/hooks
- previous 50 riddle fingerprints
- current relationship/continuity state
- locations used recently
- visual assets used recently

After a successful render, commit episode metadata and asset usage to state.

## Publishing
Final publishing must target a second social account/channel, never the Motus account.

The specific publisher connection is intentionally not wired yet. This becomes a user-action checkpoint only when:
1. the second channel exists, and
2. the user connects/authorizes it in the chosen publishing service.

## Rollout
1. Build renderer on feature branch.
2. Prepare reusable character/style assets.
3. Render episode 000 as a local/GitHub test.
4. Validate QC.
5. Wire second publishing account.
6. Run one draft/private test.
7. Merge to main.
8. Extend 22:37 master prompt to produce the fifth content package.
