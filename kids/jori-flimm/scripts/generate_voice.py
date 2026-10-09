#!/usr/bin/env python3
"""Create German Victoria narration via the free public Hugging Face CPU demo.

This sends the episode narration to the public Space. Use only story text
intended for publication.
"""
import json
import re
import subprocess
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

SPACE_ID = "nam194/KokoroTTS-HF-CPU"
SPACE_HOST = "nam194-kokorotts-hf-cpu.hf.space"
SPACE_URL = f"https://{SPACE_HOST}"
MAX_GUEST_CHARS = 280  # The Space currently truncates anonymous text at 300 chars.
VOICE_ID = "df_victoria"
SPEED = 0.92
PAUSE_SECONDS = 0.22
PAUSE_MARKER = re.compile(r"\\[\\[PAUSE:([0-9]+(?:\\.[0-9]+)?)\\]\\]")
MAX_AUDIO_BYTES = 25 * 1024 * 1024


def split_text(text: str) -> list[str]:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]
    chunks: list[str] = []
    for sentence in sentences:
        while len(sentence) > MAX_GUEST_CHARS:
            cut = sentence.rfind(" ", 0, MAX_GUEST_CHARS + 1)
            if cut < 1:
                cut = MAX_GUEST_CHARS
            chunks.append(sentence[:cut].strip())
            sentence = sentence[cut:].strip()
        if sentence:
            chunks.append(sentence)
    if not chunks or any(len(chunk) > MAX_GUEST_CHARS for chunk in chunks):
        raise SystemExit("Unable to split narration within the public demo's guest limit.")
    return chunks


def call_space(text: str) -> str:
    payload = json.dumps({
        "data": [text, "Single", VOICE_ID, "af_bella", SPEED, 0.5]
    }).encode("utf-8")
    req = Request(
        f"{SPACE_URL}/gradio_api/call/generate",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "jori-flimm-renderer"},
        method="POST",
    )
    with urlopen(req, timeout=60) as response:
        started = json.loads(response.read().decode("utf-8"))
    event_id = started.get("event_id")
    if not event_id:
        raise SystemExit(f"The voice demo returned no request ID: {started}")

    req = Request(
        f"{SPACE_URL}/gradio_api/call/generate/{event_id}",
        headers={"User-Agent": "jori-flimm-renderer", "Accept": "text/event-stream"},
    )
    with urlopen(req, timeout=300) as response:
        events = response.read().decode("utf-8")

    event_name = ""
    data_line = ""
    for line in events.splitlines():
        if line.startswith("event:"):
            event_name = line.partition(":")[2].strip()
        elif line.startswith("data:"):
            data_line = line.partition(":")[2].strip()
            if event_name == "complete":
                break
    if event_name != "complete" or not data_line:
        raise SystemExit(f"Voice demo did not complete successfully: {events[-1000:]}")
    try:
        output = json.loads(data_line)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Voice demo returned invalid JSON: {exc}")
    if not isinstance(output, list) or not output or not isinstance(output[0], dict):
        raise SystemExit(f"Unexpected voice demo response: {output}")
    audio_url = output[0].get("url")
    parsed = urlparse(audio_url or "")
    if parsed.scheme != "https" or parsed.netloc != SPACE_HOST or not parsed.path.startswith("/gradio_api/file="):
        raise SystemExit("The voice demo returned an unexpected audio URL.")
    return audio_url


def main() -> None:
    payload = json.loads(Path("work/payload.json").read_text(encoding="utf-8"))
    voice = payload.get("voice", {})
    if voice.get("provider") != "Hugging Face Spaces CPU TTS":
        raise SystemExit("Episode must explicitly select the free Victoria TTS provider.")
    if voice.get("model") != "kikiri-tts/kikiri-german-victoria" or voice.get("speaker_id") != VOICE_ID:
        raise SystemExit("Episode voice configuration does not match the licensed Victoria model.")

    narration = payload["narration"].strip()
    segments = []
    cursor = 0
    for match in PAUSE_MARKER.finditer(narration):
        speech = narration[cursor:match.start()].strip()
        if speech:
            segments.append({"kind": "speech", "text": speech})
        seconds = float(match.group(1))
        if not 5 <= seconds <= 10:
            raise SystemExit("Explicit riddle pauses must be 5-10 seconds.")
        segments.append({"kind": "pause", "duration": seconds})
        cursor = match.end()
    remainder = narration[cursor:].strip()
    if remainder:
        segments.append({"kind": "speech", "text": remainder})
    if not segments or any(item["kind"] == "speech" and "[[PAUSE:" in item["text"] for item in segments):
        raise SystemExit("Narration pause marker is malformed.")
    marker_count = len(PAUSE_MARKER.findall(narration))
    if marker_count != int(float(payload.get("riddle", {}).get("pause_seconds", 0)) >= 5):
        raise SystemExit("Narration pause marker must match the configured riddle pause.")

    out_dir = Path("work/tts-chunks")
    out_dir.mkdir(parents=True, exist_ok=True)
    sequence = []
    chunk_number = 0
    for segment in segments:
        if segment["kind"] == "pause":
            sequence.append({"kind": "pause", "duration": segment["duration"]})
            continue
        chunks = split_text(segment["text"])
        for index, chunk in enumerate(chunks):
            chunk_number += 1
            print(f"Generating Victoria narration chunk {chunk_number} ({len(chunk)} chars)", flush=True)
            try:
                audio_url = call_space(chunk)
                req = Request(audio_url, headers={"User-Agent": "jori-flimm-renderer"})
                with urlopen(req, timeout=60) as response:
                    raw = response.read(MAX_AUDIO_BYTES + 1)
                if len(raw) > MAX_AUDIO_BYTES:
                    raise SystemExit("A narration chunk exceeded 25 MiB.")
                raw_path = out_dir / f"{chunk_number:02d}-raw.wav"
                raw_path.write_bytes(raw)
                wav_path = out_dir / f"{chunk_number:02d}.wav"
                subprocess.run(
                    ["ffmpeg", "-y", "-v", "error", "-i", str(raw_path), "-ar", "24000", "-ac", "1", str(wav_path)],
                    check=True,
                )
                duration = float(subprocess.check_output([
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", str(wav_path)
                ], text=True))
                sequence.append({"kind": "speech", "text": chunk, "file": str(wav_path), "duration": duration})
                if index < len(chunks) - 1:
                    sequence.append({"kind": "pause", "duration": PAUSE_SECONDS})
            except (HTTPError, URLError, TimeoutError) as exc:
                raise SystemExit(f"Voice service request failed for chunk {chunk_number}: {exc}") from exc
            if chunk_number < len(split_text(narration.replace(PAUSE_MARKER.pattern, ""))):
                time.sleep(0.5)

    silence_cache = {}
    for item in sequence:
        if item["kind"] == "pause":
            key = f"{float(item['duration']):.2f}"
            if key not in silence_cache:
                silence = out_dir / f"pause-{key.replace('.', '-')}.wav"
                subprocess.run([
                    "ffmpeg", "-y", "-v", "error", "-f", "lavfi",
                    "-i", "anullsrc=r=24000:cl=mono", "-t", key,
                    "-c:a", "pcm_s16le", str(silence),
                ], check=True)
                silence_cache[key] = silence
            item["file"] = str(silence_cache[key])

    concat_file = out_dir / "concat.txt"
    timeline = []
    cursor = 0.0
    with concat_file.open("w", encoding="utf-8") as f:
        for item in sequence:
            path = Path(item["file"]).resolve()
            f.write(f"file '{path.as_posix()}'\\n")
            start = cursor
            cursor += float(item["duration"])
            timeline.append({
                "kind": item["kind"],
                "text": item.get("text", ""),
                "start": round(start, 3),
                "end": round(cursor, 3),
                "duration": round(float(item["duration"]), 3),
            })
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
        "-i", str(concat_file), "-c", "copy", "work/narration_source.wav",
    ], check=True)
    Path("work/voice-timeline.json").write_text(
        json.dumps({"items": timeline, "duration": round(cursor, 3)}, ensure_ascii=False, indent=2) + "\\n",
        encoding="utf-8",
    )
    explicit = sum(float(item["duration"]) for item in sequence if item["kind"] == "pause" and float(item["duration"]) >= 5)
    print(f"Generated {chunk_number} Victoria narration chunks; explicit riddle silence={explicit:.1f}s.", flush=True)

if __name__ == "__main__":
    main()
