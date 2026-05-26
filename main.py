import RobotHearing
import RobotSeeing
import RobotNavigator  # Your new A* logic file
import time
import pyttsx3

# =====================================================================
# 1. HARDWARE MOCK CONTROLLER
# =====================================================================
# This replaces the non-existent 'robot_dog_sdk'. It allows the code to
# run safely on your laptop without crashing while your PuppyPi charges.
try:
    import rospy
    from geometry_msgs.msg import Twist
    USING_REAL_ROBOT = True
    print("[System] ROS detected! Running in REAL ROBOT mode.")
except ModuleNotFoundError:
    USING_REAL_ROBOT = False
    print("[System] ROS not found. Running in LAPTOP SIMULATION mode.")
# ----------------------------

# =====================================================================
# 1. HARDWARE CONTROLLER (HANDLES BOTH REAL AND MOCK)
# =====================================================================
class MockPuppyPiController:
    def __init__(self, ip):
        self.ip = ip
        if USING_REAL_ROBOT:
            # Real Robot Initializer
            rospy.init_node('blind_guide_main', anonymous=True)
            self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
            print(f"[Hardware] Connected to PHYSICAL PuppyPi at {self.ip}")
        else:
            # Laptop Simulation Initializer
            print(f"[Simulation] Connected to VIRTUAL PuppyPi at {self.ip}")

    def move_forward(self):
        if USING_REAL_ROBOT:
            move_cmd = Twist()
            move_cmd.linear.x = 0.1  # Physical speed
            self.vel_pub.publish(move_cmd)
        else:
            print("[Simulation Physical Movement] Dog walking forward!")

    def turn_left(self):
        if USING_REAL_ROBOT:
            move_cmd = Twist()
            move_cmd.angular.z = 0.3  # Physical turn
            self.vel_pub.publish(move_cmd)
        else:
            print("[Simulation Physical Movement] Dog pivoting left!")

    def turn_right(self):
        if USING_REAL_ROBOT:
            move_cmd = Twist()
            move_cmd.angular.z = -0.3
            self.vel_pub.publish(move_cmd)
        else:
            print("[Simulation Physical Movement] Dog pivoting right!")

    def stop(self):
        if USING_REAL_ROBOT:
            self.vel_pub.publish(Twist())  # Sends zero movement
        else:
            print("[Simulation Physical Movement] Dog stopping joints.")

# =====================================================================
# 2. AUDIO SPEECH UTILITY
# =====================================================================
def robot_speak(text):
    """Voice output for the user."""
    print(f"[Voice] {text}")
    try:
        temp_engine = pyttsx3.init()
        temp_engine.setProperty('rate', 170)
        temp_engine.say(text)
        temp_engine.runAndWait()
        temp_engine.stop()
    except Exception as e:
        print(f"[Voice Error]: {e}")

# =====================================================================
# 3. VOICE NLP TARGET EXTRACTION
# =====================================================================
def extract_target(command, valid_names):
    clean = command.lower().replace("?", "").replace(".", "").strip()
    words = clean.split()
    ignore = ["find", "look", "for", "the", "a", "an", "can", "you", "please", "navigate"]
    targets = [w for w in words if w in valid_names and w not in ignore]
    return targets[0] if targets else None

# =====================================================================
# 4. MAIN CONTROL ROUTINE
# =====================================================================
def run_robot():
    # Build vocabulary library straight from your YOLO configuration parameters
    yolo_vocab = list(RobotSeeing.model.names.values())
    robot_speak("System online. How can I help you today? Bark bark!")
    
    # Initialize the fake dog connection mapping utilizing its network IP
    ROBOT_IP = "172.16.144.136"
    my_dog = MockPuppyPiController(ip=ROBOT_IP)
    
    while True:
        robot_speak("I am listening. Bark bark!")
        time.sleep(0.2) 
        command = RobotHearing.get_voice_command(duration=4)
        
        if not command or len(command.strip()) < 2:
            continue
            
        target = extract_target(command, yolo_vocab)
        
        if target:
            robot_speak(f"Searching for {target}. I will guide you once I find a path. Roof roof!")
            navigating = True
            
            # Start position in our virtual 10x10 grid layout (center bottom)
            current_pos = (5, 0) 
            
            while navigating:
                # 1. Run live Computer Vision object scan
                is_visible = RobotSeeing.look_for_object_single_frame(target)
                
                if is_visible:
                    # 2. Pathfinding Logic Execution Block
                    # Target default mapping coordinates on the upper bounds of our matrix
                    goal_pos = (5, 9) 
                    
                    # Generate fresh node list path array using the A* navigation module
                    path = RobotNavigator.get_path(current_pos, goal_pos, obstacle_list=[])
                    
                    # FIX VERIFICATION: Verify 'path' variable structure before stepping
                    if path and len(path) > 1:
                        next_step = path[1] # Extract the target adjacent tile
                        print(f"[Nav] Moving from {current_pos} to {next_step}")
                        
                        # --- ROBOT PHYSICAL MOVEMENT TRANSLATION ---
                        dx = next_step[0] - current_pos[0]
                        dy = next_step[1] - current_pos[1]
                        
                        if dx > 0:
                            my_dog.move_forward()
                        elif dy > 0:
                            my_dog.turn_right()
                        elif dy < 0:
                            my_dog.turn_left()
                        # -------------------------------------------
                        
                        # Set current step coordinate tracking as historical position reference
                        current_pos = next_step
                        robot_speak("Step forward. I am leading the way. Woof!")
                    else:
                        my_dog.stop()
                        robot_speak("The path is blocked. Please wait. Grrr!")
                else:
                    my_dog.stop()
                    print(f"[System] {target} not in view. Scanning environment...")

                # 3. Live Feedback / Emergency Voice Check Loop
                feedback = RobotHearing.get_voice_command(duration=2)
                if any(p in feedback.lower() for p in ["thank you", "thanks", "stop"]):
                    my_dog.stop()
                    robot_speak("Target reached! Give me treats! Woof woof!")
                    RobotSeeing.close_windows()
                    navigating = False 
        else:
            robot_speak("I don't know what that is. Bark!")

if __name__ == "__main__":
    run_robot()