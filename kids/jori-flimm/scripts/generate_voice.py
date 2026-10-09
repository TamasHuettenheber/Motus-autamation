#!/usr/bin/env python3
"""Create German Victoria narration through the free public CPU demo.

This sends the episode narration to the public Hugging Face Space. Episode story
text is intended for publication; do not use this path for private narration.
"""
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from gradio_client import Client

SPACE = "nam194/KokoroTTS-HF-CPU"
SPACE_URL = "https://nam194-kokorotts-hf-cpu.hf.space"
MAX_GUEST_CHARS = 280  # Space currently truncates anonymous requests at 300.
VOICE_ID = "df_victoria"
PAUSE_SECONDS = 0.22


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


def save_api_audio(result, out_path: Path) -> None:
    # Gradio Audio may return a local file, FileData mapping, or (sample_rate, samples).
    if isinstance(result, (str, Path)):
        shutil.copyfile(str(result), out_path)
        return
    if isinstance(result, dict):
        path = result.get("path")
        if path and Path(path).is_file():
            shutil.copyfile(path, out_path)
            return
        raise SystemExit(f"Gradio returned no local audio file: {result}")
    if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], (int, float)):
        sample_rate, samples = result
        sf.write(str(out_path), np.asarray(samples), int(sample_rate))
        return
    raise SystemExit(f"Unsupported audio result from Gradio: {type(result).__name__}")


def main() -> None:
    payload_path = Path("work/payload.json")
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    voice = payload.get("voice", {})
    if voice.get("provider") != "Hugging Face Spaces CPU TTS":
        raise SystemExit("Episode must explicitly select the Hugging Face free TTS provider.")
    if voice.get("model") != "kikiri-tts/kikiri-german-victoria" or voice.get("speaker_id") != VOICE_ID:
        raise SystemExit("Episode voice configuration does not match the licensed Victoria model.")
    text = payload["narration"].strip()
    chunks = split_text(text)
    Path("work/tts-chunks").mkdir(parents=True, exist_ok=True)
    client = Client(SPACE_URL, verbose=False, max_workers=1)
    normalized: list[Path] = []
    speed = float(voice.get("speed", 0.92))

    for index, chunk in enumerate(chunks, start=1):
        print(f"Generating Victoria narration chunk {index}/{len(chunks)} ({len(chunk)} chars)")
        result = client.predict(
            chunk, "Single", VOICE_ID, "af_bella", speed, 0.5,
            api_name="/generate",
        )
        raw = Path(f"work/tts-chunks/{index:02d}-raw.wav")
        save_api_audio(result, raw)
        wav = Path(f"work/tts-chunks/{index:02d}.wav")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-ar", "24000", "-ac", "1", str(wav)],
            check=True,
        )
        normalized.append(wav)

    segments: list[np.ndarray] = []
    for index, wav in enumerate(normalized):
        audio, sample_rate = sf.read(str(wav), dtype="float32")
        if sample_rate != 24000:
            raise SystemExit(f"Unexpected sample rate {sample_rate} in {wav}")
        if audio.ndim == 2:
            audio = audio.mean(axis=1)
        if index:
            segments.append(np.zeros(int(PAUSE_SECONDS * sample_rate), dtype=np.float32))
        segments.append(audio)

    combined = np.concatenate(segments)
    sf.write("work/narration_source.wav", combined, 24000, subtype="PCM_16")
    print(f"Generated {len(chunks)} Victoria chunks, {len(combined)/24000:.1f}s total.")


if __name__ == "__main__":
    main()
