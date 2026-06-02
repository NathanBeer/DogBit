import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
import scipy.io.wavfile as wav

model = whisper.load_model("base")

def get_voice_command(duration=4):
    fs = 16000
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        wav.write(tmp_file.name, fs, (recording * 32767).astype(np.int16))
        path = tmp_file.name
    
    result = model.transcribe(path, fp16=False)
    os.remove(path)
    return result["text"].strip().lower()