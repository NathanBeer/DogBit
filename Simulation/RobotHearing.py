import speech_recognition as sr
import whisper
import os

# Load the model globally so it only loads once
print("[System] Loading Whisper model...")
model = whisper.load_model("tiny")
print("[System] Model loaded successfully.")

def listen_for_command():
    # Use card 1 based on your 'arecord -l' output
    mic = sr.Microphone(device_index=1)
    recognizer = sr.Recognizer()
    
    with mic as source:
        print("[Hearing] Listening (Speak now)...")
        try:
            # Adjust for ambient noise and listen for a command
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            # Save audio to a temporary file
            with open("input.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            print("[Hearing] Transcribing...")
            result = model.transcribe("input.wav")
            print(f"[Hearing] User said: {result['text']}")
            return result["text"].lower()
            
        except Exception as e:
            print(f"[Hearing] Audio Error: {e}")
            return ""