import speech_recognition as sr
import time

def get_voice_command(duration=4):
    """Listens for voice input using the WM8960 soundcard."""
    r = sr.Recognizer()
    
    # 16000Hz is the native sample rate for the WM8960 HAT
    # Index 1 is standard for this HAT, but if it fails, check list_microphone_names()
    mic = sr.Microphone(device_index=1, sample_rate=16000)
    
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print(f"[Hearing] Listening for {duration} seconds...")
            
            # Timeout/phrase_time_limit prevents the hang
            audio = r.listen(source, timeout=5, phrase_time_limit=duration)
            
            print("[Hearing] Transcribing...")
            text = r.recognize_google(audio)
            print(f"[Hearing] Captured: '{text}'")
            return text.lower()
            
    except Exception as e:
        # Return empty string on failure so main loop continues
        return ""