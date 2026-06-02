import RobotHearing
import RobotSeeing
import RobotNavigator
import time
import os
from gtts import gTTS

# Placeholder for direct hardware interface 
class LocalRobotController:
    def move_forward(self): print("[Hardware] Moving forward")
    def turn_left(self): print("[Hardware] Turning left")
    def turn_right(self): print("[Hardware] Turning right")
    def stop(self): print("[Hardware] Stopped")

my_dog = LocalRobotController()

def robot_speak(text):
    print(f"[Voice] {text}")
    tts = gTTS(text=text, lang='en')
    tts.save("speech.mp3")
    # Using 'mpg123 -q' for quiet output to avoid terminal clutter
    os.system("mpg123 -q speech.mp3")

def run_robot():
    while True:
        robot_speak("Where would you like me to go?")
        # Whisper transcription
        raw_command = RobotHearing.get_voice_command(duration=4)
        print(f"[DEBUG] Robot heard: '{raw_command}'")
        
        # Flexible matching: search for 'person' if it's in the command
        target = "person" if "person" in raw_command else None
        
        if not target:
            robot_speak("I didn't understand which target you want me to find.")
            continue
            
        # Search loop (360 spin)
        robot_speak(f"Searching for {target}.")
        found = False
        # Rotate and check 8 times (roughly 45 degrees per check)
        for i in range(8):
            print(f"[Search] Attempt {i+1}/8...")
            if RobotSeeing.look_for_object_single_frame(target):
                found = True
                break
            my_dog.turn_left()
            time.sleep(1.0) # Pause to let camera settle
            
        if not found:
            robot_speak("I could not find the target.")
            continue
            
        # Navigation
        current_pos = (0, 0)
        goal_pos = (5, 5) 
        robot_speak("Target found. Navigating.")
        
        # Navigate towards the found object
        path = RobotNavigator.get_path(current_pos, goal_pos)
        if path and len(path) > 1:
            for node in path[1:]:
                my_dog.move_forward()
                current_pos = (node.x, node.y)
                time.sleep(0.5)
            robot_speak("I have arrived. Now give me a treat! Bark bark")
        else:
            robot_speak("I am already at the target.")
            
        # Follow-up
        robot_speak("Is there anything else you would like me to do? Bark bark")
        response = RobotHearing.get_voice_command(duration=3)
        if "no" in response.lower():
            robot_speak("Going to sleep now. Goodbye.")
            break

if __name__ == "__main__":
    run_robot()