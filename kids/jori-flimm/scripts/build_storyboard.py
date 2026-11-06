#!/usr/bin/env python3
"""Create a six-scene, NON-PUBLISHABLE story preview from existing licensed series art.

This deliberately makes styled montages of old art. It does NOT claim that the
pictures are newly illustrated or that they match each scene brief. The output
is a preview package, never an approved renderer or social-media payload.
"""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / "assets"
SOURCES = ([ROOT / "e000" / ("scene-%02d.jpg" % n) for n in range(1, 7)] +
           [ROOT / "e001" / ("scene-%02d.png" % n) for n in range(1, 7)])

WIDTH, HEIGHT = 720, 1280
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
]


def text_font(size):
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def validate_draft(d):
    if not isinstance(d, dict):
        raise ValueError("Draft must be a JSON object")
    required = ["date", "episode_number", "title", "narration", "scene_briefs", "riddle"]
    for key in required:
        if key not in d:
            raise ValueError(f"Missing field: {key}")
    if d.get("approved_for_publish") is not False:
        raise ValueError("Only deliberately unpublished drafts are accepted")
    if d.get("status") != "draft_requires_illustration_and_qc":
        raise ValueError("Wrong preview draft status")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(d["date"])):
        raise ValueError("Invalid episode date")
    if not isinstance(d["episode_number"], int) or d["episode_number"] < 0:
        raise ValueError("Invalid episode number")
    if not isinstance(d["scene_briefs"], list) or len(d["scene_briefs"]) != 6:
        raise ValueError("Exactly six scene briefs are required")
    if any(not isinstance(x, str) or len(x.strip()) < 25 for x in d["scene_briefs"]):
        raise ValueError("Invalid scene brief")
    if not all(p.exists() for p in SOURCES):
        raise FileNotFoundError("Source illustrations missing; no placeholder accepted")


def make_scene(source, dst, episode_number, scene_number, title):
    with Image.open(source) as opened:
        orig = opened.convert("RGB")
    # Controlled crop variation retains central character and avoids blank bars.
    w, h = orig.size
    displacement = ((episode_number * 3 + scene_number) % 5 - 2) * 0.018
    x = int(w * max(0, min(1, .5 + displacement)))
    im = ImageOps.fit(orig, (WIDTH, HEIGHT), Image.Resampling.LANCZOS, centering=(x / max(w, 1), .48))
    im = ImageEnhance.Color(im).enhance([.95, 1.0, 1.05][scene_number % 3])
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rectangle((0, 0, WIDTH, 170), fill=(12, 24, 52, 170))
    gd.rectangle((0, HEIGHT - 145, WIDTH, HEIGHT), fill=(12, 24, 52, 185))
    # Deterministic glowing particles, without pretending to draw new characters.
    for j in range(9):
        seed = hashlib.sha256(f"{episode_number}-{scene_number}-{j}".encode()).digest()
        cx = 35 + seed[0] * (WIDTH - 70) // 255
        cy = 210 + seed[1] * (HEIGHT - 420) // 255
        radius = 2 + seed[2] % 4
        gd.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(255, 231, 165, 115))
    im = Image.alpha_composite(im.convert("RGBA"), glow)
    draw = ImageDraw.Draw(im)
    label = f"JORI & FLIMM  •  FOLGE {episode_number:03d}"
    draw.text((32, 33), label, font=text_font(23), fill="#ffe9b0")
    # First (chapter) and last (continuation) scene have distinct headline panels.
    if scene_number == 1:
        text = str(title).strip()[:65]
    elif scene_number == 6:
        text = "Morgen geht das Abenteuer weiter!"
    else:
        text = f"Szene {scene_number} / 6"
    max_len = 38
    lines = [text[:max_len]]
    if len(text) > max_len:
        lines.append(text[max_len:max_len*2].strip())
    for i, line in enumerate(lines):
        draw.text((32, HEIGHT - 118 + i * 36), line,
                  font=text_font(27 if scene_number in (1, 6) else 22), fill="white")
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(dst, format="JPEG", quality=83, optimize=True, progressive=True)
    with Image.open(dst) as verify:
        if verify.size != (WIDTH, HEIGHT):
            raise RuntimeError("Preview image dimensions do not match")


def build(draft_path, out_root):
    data = json.loads(Path(draft_path).read_text(encoding="utf-8"))
    validate_draft(data)
    episode_number = data["episode_number"]
    folder = out_root / f"{data['date']}-e{episode_number:03d}"
    if folder.exists():
        raise FileExistsError(f"Preview already exists: {folder}")
    if any(folder.parent.glob(f"*-e{episode_number:03d}")):
        raise FileExistsError("This episode already has a visual preview")
    sources = [(episode_number * 7 + k * 5) % len(SOURCES) for k in range(6)]
    # Six unique illustrations per episode, but still a finite recurring pool.
    assets = []
    for i, source_index in enumerate(sources, start=1):
        name = f"scene-{i:02d}.jpg"
        img = folder / name
        make_scene(SOURCES[source_index], img, episode_number, i, data["title"])
        assets.append({
            "order": i,
            "file": name,
            "source_art": SOURCES[source_index].relative_to(BASE).as_posix(),
            "scene_brief": data["scene_briefs"][i - 1],
            "art_alignment_confirmed": False,
            "width": WIDTH,
            "height": HEIGHT
        })
    metadata = {
        "date": data["date"],
        "episode_number": episode_number,
        "title": data["title"],
        "status": "PREVIEW_ONLY",
        "approved_for_publish": False,
        "visual_origin": "styled_montage_of_existing_series_illustrations",
        "new_unique_scene_illustrations": False,
        "story_specific_visuals_verified": False,
        "audio_generated": False,
        "video_rendered": False,
        "scheduled_for_tiktok": False,
        "intended_publish_time": "14:00 Europe/Berlin",
        "scenes": assets,
    }
    (folder / "preview-manifest.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=BASE / "previews")
    args = parser.parse_args()
    dest = build(args.draft, args.output_dir)
    print(f"STORYBOARD_PREVIEW_ONLY {dest}; not a video or TikTok post")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, FileNotFoundError, FileExistsError) as err:
        print(f"PREVIEW_BLOCKED: {err}", file=sys.stderr)
        sys.exit(1)
