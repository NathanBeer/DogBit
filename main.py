import sys
import os
# Silence ALSA audio errors
sys.stderr = open(os.devnull, 'w')

import RobotHearing
import RobotSeeing
import RobotMovement
import RobotNavigator
import time
from gtts import gTTS

def robot_speak(text):
    print(f"[Voice] {text}")
    tts = gTTS(text=text, lang='en')
    tts.save("speech.mp3")
    os.system("mpg123 -q speech.mp3")

def find_and_approach(target):
    # 1. SEARCH: Rotate until object is in view
    robot_speak(f"Searching for {target}.")
    found = False
    
    # 360-degree search
    for _ in range(360): 
        if RobotSeeing.is_object_in_view(target):
            found = True
            break
        RobotMovement.rotate_step() 
        
    if not found:
        robot_speak("I could not find it.")
        return False

    # 2. APPROACH: Use A* Pathfinding
    robot_speak("I found it. Calculating path. Bark bark!")
    
    # Get start (0,0) and target (from YOLO)
    start_pos = (0, 0)
    end_pos = RobotSeeing.get_coords(target) 
    
    path = RobotNavigator.get_path(start_pos, end_pos)
    
    # Follow the path steps
    for step in path:
        print(f"Moving to: {step}")
        # RobotMovement.move_to(step) 
        
    robot_speak("We got to the destination, now give me a treat!")
    return True

def run_robot():
    while True:
        robot_speak("What would you like me to find? Roof, roof")
        command = RobotHearing.get_voice_command()
        
        # Match voice command to objects YOLO can see
        target = RobotSeeing.match_target(command) 
        
        if target:
            find_and_approach(target)
            
            # 3. LOOP: Anything else?
            robot_speak("Is there anything else you would like me to find? Bark bark")
            response = RobotHearing.get_voice_command()
            
            if "yes" in response.lower():
                continue # Loops back to the start
            else:
                robot_speak("Goodnight!")
                break # Shutdown
        else:
            robot_speak("I didn't catch that.")

if __name__ == "__main__":
    run_robot()