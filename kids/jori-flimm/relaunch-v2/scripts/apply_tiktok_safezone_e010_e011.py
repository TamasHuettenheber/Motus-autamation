#!/usr/bin/env python3
"""Place the puzzle question and every answer clue inside TikTok's safe zone.

This is an idempotent post-render correction for episodes 010 and 011.  It keeps
the approved Sulafat audio, subtitles, duration and scene timing unchanged.
"""
import argparse
import math
import os
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path.cwd()
SAFE_RIGHT = 540
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(F_BOLD, size)


def star_points(cx, cy, outer, inner):
    points = []
    for index in range(10):
        radius = outer if index % 2 == 0 else inner
        angle = -math.pi / 2 + index * math.pi / 5
        points.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
    return points


def draw_base():
    image = Image.new("RGBA", (720, 1280), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Hide the former wide question banner on the right.  This rectangle has no
    # information; all meaningful puzzle content remains left of x=540.
    draw.rectangle((540, 132, 720, 250), fill=(13, 32, 56, 238))
    # One self-contained puzzle board.  Its complete alpha bounding box ends at
    # x=540, leaving x=560..719 clear for TikTok's interaction controls.
    draw.rounded_rectangle((42, 132, SAFE_RIGHT, 805), radius=26,
                           fill=(13, 32, 56, 238), outline=(246, 211, 127, 255), width=4)
    return image, draw


def episode_010_overlay(path):
    image, draw = draw_base()
    draw.text((291, 190), "WELCHE KUGEL", font=font(27), anchor="mm", fill="#fff2c9")
    draw.text((291, 228), "LEUCHTET ZUERST?", font=font(27), anchor="mm", fill="#fff2c9")
    centers = (126, 291, 456)
    colors = ("#57bfff", "#e9f4ff", "#ffc85c")
    labels = ("BLAU", "SILBERN", "GOLD")
    for x, color, label in zip(centers, colors, labels):
        draw.rounded_rectangle((x - 65, 310, x + 65, 560), radius=18,
                               fill=(26, 49, 76, 255), outline=(242, 220, 165, 255), width=3)
        draw.ellipse((x - 43, 352, x + 43, 438), fill=color, outline="#ffffff", width=4)
        draw.text((x, 508), label, font=font(19), anchor="mm", fill="white")
    draw.text((291, 640), "BLAU  →  SILBERN  →  GOLD", font=font(21), anchor="mm", fill="#fff2c9")
    image.save(path)


def episode_011_overlay(path):
    image, draw = draw_base()
    draw.text((291, 188), "WELCHE FORM PASST", font=font(25), anchor="mm", fill="#fff2c9")
    draw.text((291, 224), "IN DIE LÜCKE?", font=font(25), anchor="mm", fill="#fff2c9")
    draw.rounded_rectangle((225, 275, 357, 417), radius=18,
                           fill=(26, 49, 76, 255), outline=(242, 220, 165, 255), width=3)
    draw.polygon(star_points(291, 346, 45, 20), fill="#62c9f2", outline="#ffffff")
    centers = (126, 291, 456)
    for x in centers:
        draw.rounded_rectangle((x - 65, 480, x + 65, 686), radius=18,
                               fill=(26, 49, 76, 255), outline=(242, 220, 165, 255), width=3)
    draw.ellipse((92, 535, 160, 603), outline="#eefaff", width=7)
    draw.polygon(star_points(291, 570, 39, 17), fill="#ffd86a", outline="#ffffff")
    draw.ellipse((422, 535, 490, 603), fill="#eefaff")
    draw.ellipse((446, 518, 506, 578), fill=(26, 49, 76, 255))
    for x, label in zip(centers, ("RING", "STERN", "MOND")):
        draw.text((x, 645), label, font=font(18), anchor="mm", fill="white")
    image.save(path)


def long_silence(video):
    process = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(video), "-af",
         "silencedetect=noise=-60dB:d=6", "-f", "null", "-"],
        text=True, capture_output=True, check=True,
    )
    starts = [float(x) for x in re.findall(r"silence_start:\s*([0-9.]+)", process.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", process.stderr)]
    durations = [float(x) for x in re.findall(r"silence_duration:\s*([0-9.]+)", process.stderr)]
    matches = [(a, b, d) for a, b, d in zip(starts, ends, durations) if 6.8 <= d <= 7.2]
    assert len(matches) == 1, matches
    return matches[0]


def apply(video, overlay):
    start, end, duration = long_silence(video)
    temporary = video.with_suffix(".safezone.tmp.mp4")
    subprocess.run([
        "ffmpeg", "-nostdin", "-y", "-loglevel", "error",
        "-i", str(video), "-i", str(overlay),
        "-filter_complex", f"[0:v][1:v]overlay=0:0:enable='between(t,{start:.6f},{end:.6f})'[v]",
        "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "21", "-pix_fmt", "yuv420p", "-r", "24", "-c:a", "copy",
        "-movflags", "+faststart", str(temporary)
    ], check=True)
    os.replace(temporary, video)
    start2, end2, duration2 = long_silence(video)
    assert abs(duration2 - 7.0) <= 0.2
    print(f"JORI_TIKTOK_SAFEZONE_OK video={video} overlay_right={SAFE_RIGHT} "
          f"pause={duration2:.6f} range={start2:.6f}-{end2:.6f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=int, required=True, choices=[10, 11])
    args = parser.parse_args()
    if args.episode == 10:
        video = ROOT / "published/jori-flimm-2026-10-31-e010-v2.mp4"
    else:
        video = ROOT / "published/jori-flimm-2026-11-01-e011-v1.mp4"
    assert video.is_file() and video.stat().st_size > 1_000_000
    asset_dir = ROOT / "kids/jori-flimm/relaunch-v2/assets/tiktok-safezone"
    asset_dir.mkdir(parents=True, exist_ok=True)
    overlay = asset_dir / f"e{args.episode:03d}-puzzle-overlay.png"
    (episode_010_overlay if args.episode == 10 else episode_011_overlay)(overlay)
    apply(video, overlay)


if __name__ == "__main__":
    main()
