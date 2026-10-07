# Jori & Flimm – Kids Short-Story Pipeline

Status: design/build branch. The live Motus workflows on `main` stay untouched until the kids pipeline passes an end-to-end test.

## Decision
Keep this pipeline in the existing Motus automation repository because it will share the same ChatGPT master trigger and the same GitHub infrastructure. Keep all kids content isolated below `kids/jori-flimm/` and use separate GitHub workflows and output paths.

## Product rule
The KDP book content stays exclusive to the book/e-book. The video channel must NOT retell, reveal, serialize, or solve the 24 book missions.

The video series uses the same world and characters but tells original prequel/side stories.

## Canonical world
- Series: Jori & Flimm – Rätselwelten
- Core characters: Jori, Flimm; Murrflaum may be introduced only when story continuity makes sense
- World: Flockenfels
- Target age: 7–10
- Format target: 60–90 second vertical short
- Content: original mini-story + one age-appropriate riddle + reveal/cliffhanger
- Publish target: 16:00 local time
- Production target: previous evening in the 22:37 master production run

## Free-first production
Initial format is slideshow/2.5D motion:
- 6–9 still images
- 8–15 seconds per image
- slow zoom/pan (Ken Burns)
- narration
- low-volume background music
- on-screen riddle and answer
- subtitles
- no paid AI-video generation

## Isolation
Do not modify live Motus rendering logic until:
1. one kids episode renders successfully,
2. QC passes,
3. second-channel publishing is connected,
4. one private/unlisted or draft posting test succeeds.

See:
- `series-bible.md`
- `pipeline-spec.md`
- `episode-state.schema.json`
