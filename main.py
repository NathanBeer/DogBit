import RobotHearing
import RobotSeeing
import RobotNavigator
import time
import os
from gtts import gTTS

# Placeholder for direct hardware interface (e.g., Serial/ROS)
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
    os.system("mpg123 speech.mp3")

def run_robot():
    while True:
        robot_speak("Where would you like me to go?")
        # Whisper transcription
        target = RobotHearing.get_voice_command(duration=4)
        
        # Search loop (360 spin)
        robot_speak(f"Searching for {target}.")
        found = False
        for _ in range(8): # Approx 360 degrees
            if RobotSeeing.look_for_object_single_frame(target):
                found = True
                break
            my_dog.turn_left()
            time.sleep(0.5)
            
        if not found:
            robot_speak("I could not find that.")
            continue
            
        # Navigation
        current_pos = (0, 0)
        goal_pos = (5, 5) 
        robot_speak("Target found. Moving towards it.")
        
        while True:
            path = RobotNavigator.get_path(current_pos, goal_pos)
            if path and len(path) > 1:
                next_node = path[1]
                my_dog.move_forward()
                current_pos = (next_node.x, next_node.y)
                if current_pos == goal_pos: break
            else: break
            
        # Follow-up
        robot_speak("I have arrived. Thank you.")
        robot_speak("Is there anything else you would like me to do?")
        response = RobotHearing.get_voice_command(duration=3)
        if "no" in response.lower():
            robot_speak("Understood. Shutting down. Goodbye.")
            break

if __name__ == "__main__":
    run_robot()