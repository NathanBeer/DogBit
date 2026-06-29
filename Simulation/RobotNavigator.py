import time
from xgolib import XGO

# Initialize the XGO Mini robot globally
dog = XGO('xgomini')

def turn_and_scan(speed=25, duration=15):
    """Rotates the robot to scan the surroundings."""
    print(f"[Navigator] Scanning for objects...")
    start_time = time.time()
    dog.turn(speed)
    
    # Scan until time is up
    while time.time() - start_time < duration:
        # This will be interrupted if the vision module finds a target
        pass
        
    dog.stop()
    return False

def move_to_target(distance_units=50):
    """Moves the robot forward towards the detected object."""
    print(f"[Navigator] Approaching target...")
    dog.move_x(distance_units)
    time.sleep(2)
    dog.stop()

def perform_search_pattern(target_func, target_name):
    """
    Combines turning with vision detection.
    Pass the vision detection function (look_for_object) here.
    """
    print(f"[Navigator] Starting search pattern for {target_name}")
    start_time = time.time()
    
    while time.time() - start_time < 20: # 20 second search limit
        dog.turn(30)
        # Check vision module
        if target_func(target_name):
            dog.stop()
            print("[Navigator] Target locked.")
            return True
    
    dog.stop()
    return False