import whisper
import sounddevice as sd
import numpy as np

# Load once
print("[Hearing] Loading Whisper model...")
model = whisper.load_model("base")

def get_voice_command(duration=3):
    fs = 16000
    print(f"  (Listening for {duration}s...)")
    try:
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()
        audio_data = np.squeeze(audio)
        
        # Transcribe audio
        result = model.transcribe(audio_data, fp16=False)
        return result['text'].strip().lower()
    except Exception as e:
        print(f"[Hearing Error] {e}")
        return ""