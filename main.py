import RobotHearing
import RobotSeeing
import RobotNavigator
import time
import os
from gtts import gTTS

def robot_speak(text):
    print(f"[Voice] {text}")
    tts = gTTS(text=text, lang='en')
    tts.save("speech.mp3")
    os.system("mpg123 -q speech.mp3")

def run_robot():
    # Get the list of all objects the model can see
    # Assuming RobotSeeing has a function or property for this
    available_objects = RobotSeeing.get_model_classes() 
    print(f"[System] Robot can recognize: {available_objects}")
    
    while True:
        robot_speak("What would you like me to find?")
        print("Listening for command...")
        raw_command = RobotHearing.get_voice_command(duration=5)
        print(f"You want to find: {raw_command}")
        
        # Clean the input
        command_clean = raw_command.lower().strip()
        
        # Match input against available YOLO objects
        target = None
        for obj in available_objects:
            if obj in command_clean:
                target = obj
                break
        
        if not target:
            robot_speak("I don't know how to find that.")
            print(f"[Logic] Could not match '{command_clean}' to known objects.")
            continue
            
        robot_speak(f"Searching for {target}.")
        
        # Search loop
        found = False
        for i in range(8):
            if RobotSeeing.look_for_object_single_frame(target):
                found = True
                break
            # my_dog.turn_left()
            time.sleep(1.0)
            
        if found:
            robot_speak(f"I found the {target}.")
        else:
            robot_speak(f"I could not find the {target}.")

if __name__ == "__main__":
    run_robot()