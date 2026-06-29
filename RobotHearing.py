import speech_recognition as sr
import whisper
import os

# Load model outside the function to avoid re-loading
print("[System] Loading Whisper model...")
try:
    model = whisper.load_model("tiny")
except Exception as e:
    print(f"[System] Error loading Whisper: {e}")
    model = None

def listen_for_command():
    if not model: return ""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("[Hearing] Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            # Save to temporary file for Whisper
            with open("input.wav", "wb") as f:
                f.write(audio.get_wav_data())
            result = model.transcribe("input.wav", fp16=False)
            return result["text"].lower()
        except Exception as e:
            print(f"[Hearing] Error: {e}")
            return ""