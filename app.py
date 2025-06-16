import os
import sys
import time
import torch
import numpy as np
import sounddevice as sd
import soundfile as sf
import datetime
from transformers import pipeline
from kokoro import KPipeline

# Set up environment variables
os.environ["HF_HOME"] = "D:/hf_cache"
os.environ["HUGGING_FACE_HUB_TOKEN"] = "HF_TOKEN" 

#  PIPELINE SETUP

# Ultravox (Audio-to-Text + LLM) pipeline
pipe = pipeline(
    model="fixie-ai/ultravox-v0_5-llama-3_2-1b",
    # model="fixie-ai/ultravox-v0_5-llama-3_1-8b",
    trust_remote_code=True,
    resume_download=True
)

# Kokoro TTS pipeline
kokoro_pipeline = KPipeline(lang_code='a')

# AUDIO RECORDING 

def record_audio(duration=5, sr=16000):
    """
    Records microphone input for a fixed duration with a live countdown.
    """
    print("🎤 Listening...", end='', flush=True)
    recording = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')

    # Live countdown timer
    for remaining in range(duration, 0, -1):
        sys.stdout.write(f"\r🎤 Listening... {remaining}s ")
        sys.stdout.flush()
        time.sleep(1)

    sd.wait()
    print("\r✅ Recording complete!")
    return np.squeeze(recording), sr

# TTS SPEAK

def speak_kokoro(text, voice='af_heart'):
    """
    Converts text to speech using Kokoro and plays the audio.
    Each response is saved as a separate WAV file using a timestamp.
    """
    generator = kokoro_pipeline(text, voice=voice)
    
    # Unique filename
    # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # filename = f"kokoro_tts_{timestamp}.wav"

    full_audio = []
    for _, _, audio in generator:
        full_audio.extend(audio)
    
    full_audio = np.array(full_audio)
    # sf.write(filename, full_audio, 24000)  # Save audio to file
    # print(f"🔊 Saved TTS to: {filename}")

    sd.play(full_audio, 24000)
    sd.wait()

#

def main():
    print("🎙️ Voice Assistant is now running. Press Ctrl+C to stop.\n")

    try:
        while True:
            audio, sr = record_audio()

            turns = [
                {
                    "role": "system",
                    "content": (
                        "You are a friendly and helpful English-speaking AI assistant. "
                        "First, briefly repeat what the user said, then respond in English, even if the user speaks another language. "
                        "Your response should start like: 'You said: <repeat> and then the response'."
                    )
                }
            ]

            try:
                result = pipe({'audio': audio, 'turns': turns, 'sampling_rate': sr }, max_new_tokens=100)
                # print("🔍 Raw Ultravox Output:", result)  # Debug print
                
                # Extract the text output
                if isinstance(result, dict) and "text" in result:
                    text_response = result["text"]
                elif isinstance(result, list) and "generated_text" in result[0]:
                    text_response = result[0]["generated_text"]
                elif isinstance(result, str):
                    text_response = result
                else:
                    print("❌ Unexpected response format from Ultravox.")
                    continue

                print(f"🤖 Ultravox Response: {text_response}")

            except Exception as e:
                print(f"❌ Ultravox Error: {e}")
                continue

            # Speak response
            speak_kokoro(text_response)

    except KeyboardInterrupt:
        print("\n👋 Exiting program.")

if __name__ == "__main__":
    main()
