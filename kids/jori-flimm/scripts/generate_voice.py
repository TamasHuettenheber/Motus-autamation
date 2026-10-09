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

    chunks = split_text(payload["narration"].strip())
    out_dir = Path("work/tts-chunks")
    out_dir.mkdir(parents=True, exist_ok=True)
    normalized = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"Generating Victoria narration chunk {index}/{len(chunks)} ({len(chunk)} chars)", flush=True)
        try:
            audio_url = call_space(chunk)
            req = Request(audio_url, headers={"User-Agent": "jori-flimm-renderer"})
            with urlopen(req, timeout=60) as response:
                raw = response.read(MAX_AUDIO_BYTES + 1)
            if len(raw) > MAX_AUDIO_BYTES:
                raise SystemExit("A narration chunk exceeded 25 MiB.")
            raw_path = out_dir / f"{index:02d}-raw.wav"
            raw_path.write_bytes(raw)
            wav_path = out_dir / f"{index:02d}.wav"
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-i", str(raw_path), "-ar", "24000", "-ac", "1", str(wav_path)],
                check=True,
            )
            normalized.append(wav_path)
        except (HTTPError, URLError, TimeoutError) as exc:
            raise SystemExit(f"Voice service request failed for chunk {index}: {exc}") from exc
        if index < len(chunks):
            time.sleep(0.5)

    silence = out_dir / "pause.wav"
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-f", "lavfi",
        "-i", "anullsrc=r=24000:cl=mono", "-t", str(PAUSE_SECONDS),
        "-c:a", "pcm_s16le", str(silence),
    ], check=True)
    concat_file = out_dir / "concat.txt"
    with concat_file.open("w", encoding="utf-8") as f:
        for index, wav_path in enumerate(normalized):
            f.write(f"file '{wav_path.resolve().as_posix()}'\n")
            if index < len(normalized) - 1:
                f.write(f"file '{silence.resolve().as_posix()}'\n")
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
        "-i", str(concat_file), "-c", "copy", "work/narration_source.wav",
    ], check=True)
    print(f"Generated {len(chunks)} Victoria narration chunks.", flush=True)


if __name__ == "__main__":
    main()
