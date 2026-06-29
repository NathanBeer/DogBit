import time
import RobotMovement
import RobotSeeing

def perform_search_pattern(target_name, duration=15):
    """
    High-level behavior: Rotates and continuously checks for the object.
    This is non-blocking to the main logic loop.
    """
    print(f"[Navigator] Scanning for {target_name}...")
    start_time = time.time()
    
    # Start turning
    RobotMovement.rotate(speed=30, direction="right")
    
    while time.time() - start_time < duration:
        # Check camera WHILE turning
        if RobotSeeing.look_for_object(target_name):
            RobotMovement.safe_stop()
            return True
        time.sleep(0.1) # Prevents CPU hogging
            
    RobotMovement.safe_stop()
    return False