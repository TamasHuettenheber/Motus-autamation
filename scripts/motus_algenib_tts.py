"""Generate MOTUS speech with the existing Jori Gemini key."""
import os
import wave
from google import genai
from google.genai import types

key = os.environ.get("JORI_GEMINI_API_KEY")
if not key:
    raise SystemExit("Missing JORI_GEMINI_API_KEY")
text = os.environ["MOTUS_TEXT"].strip()
if not text:
    raise SystemExit("Empty narration")
response = genai.Client(api_key=key).models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents="Sprich auf Deutsch mit einer tiefen, markanten männlichen Stimme. Warm, glaubwürdig, motivierend, ohne Musik oder zusätzliche Wörter. Text: " + text,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Algenib")
            )
        ),
    ),
)
audio = response.candidates[0].content.parts[0].inline_data.data
with wave.open("work/audio_source", "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(24000)
    wav.writeframes(audio)
print("MOTUS_ALGENIB_GENERATED", len(audio))
