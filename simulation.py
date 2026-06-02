import pybullet as p
import pybullet_data
import time
import torch
import numpy as np
import random

# Initialize compute device
device = ('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')
print(f"Device initialized: {device}")

# 1. Connect to the GUI physics client
physics_client = p.connect(p.GUI)

# Set the search path so PyBullet can find "plane.urdf" and "laikago/laikago.urdf"
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 2. Set Z-axis gravity to -9.81
# The parameters are (x, y, z) gravity components
p.setGravity(0, 0, -9.81)

# Load the ground plane
plane_id = p.loadURDF("plane.urdf")

# 3. Load the Laikago robot at position [0, 0, 0.5]
# The parameters are: (URDF_path, basePosition=[x, y, z])
robot_id = p.loadURDF("laikago/laikago.urdf", basePosition=[0, 0, 0.5])

print(f"Quadruped loaded with ID: {robot_id}")

# TODO: Generate random X and Y coordinates between 2 and 5 (can be positive or negative)
target_x = 0 # REPLACE THIS LINE
target_y = 0 # REPLACE THIS LINE
target_pos = [target_x, target_y, 0.2]

# TODO: Create a visual shape of a sphere (radius 0.2, color Red: [1, 0, 0, 1])
ball_visual = None # REPLACE THIS LINE

# TODO: Create a MultiBody for the ball using the visual shape at the target_pos (mass = 0)
ball_id = None # REPLACE THIS LINE

print(f"Target spawned at: {target_pos}")

def gait_step(robot_id, forward_speed, turn_speed, phase):
    """Simplified gait controller for Laikago"""
    # 12 joints: 0-2 (FR), 3-5 (FL), 6-8 (RR), 9-11 (RL)
    joints = [1, 2, 4, 5, 7, 8, 10, 11]
    amplitude = 0.3
    for i, j_idx in enumerate(joints):
        offset = phase + (i % 2) * np.pi
        target = amplitude * np.sin(offset) * forward_speed

        # Simple turning logic by modifying left/right leg amplitudes
        if j_idx in [3, 4, 5, 9, 10, 11]: # Left legs
            target += turn_speed
        else: # Right legs
            target -= turn_speed

        p.setJointMotorControl2(robot_id, j_idx, p.POSITION_CONTROL, targetPosition=target)

print("Gait Controller initialized.")

phase = 0
reached = False

print("Starting search and rescue mission...")

for i in range(5000):
    # 1. Get current robot state (Position and Yaw angle)
    pos, ori = p.getBasePositionAndOrientation(robot_id)
    euler = p.getEulerFromQuaternion(ori)
    current_yaw = euler[2]

    # TODO: Calculate the difference in X and Y between target_pos and robot pos
    dx = 0 # REPLACE THIS LINE
    dy = 0 # REPLACE THIS LINE

    # TODO: Calculate Euclidean distance to the ball
    distance = 0 # REPLACE THIS LINE

    # TODO: Calculate the angle to the ball using np.arctan2(y, x)
    angle_to_ball = 0 # REPLACE THIS LINE

    # Calculate heading error
    heading_error = angle_to_ball - current_yaw

    # Normalize heading error to [-pi, pi] to avoid spinning in circles
    heading_error = (heading_error + np.pi) % (2 * np.pi) - np.pi

    # Package state into PyTorch tensor (Useful for future RL integration)
    state_tensor = torch.tensor([distance, heading_error], dtype=torch.float32).to(device)

    # TODO: Check if the robot has reached the ball (e.g., distance < 0.6 meters)
    # If reached, set reached = True, print a success message, and 'break' the loop.
    # INSERT YOUR IF STATEMENT HERE

    # Set forward and turn speeds based on calculated errors
    fwd_v = 1.0 if abs(heading_error) < 0.5 else 0.1
    turn_v = heading_error * 2.0

    # Apply movement via our gait controller
    gait_step(robot_id, fwd_v, turn_v, phase)
    phase += 0.1

    # Advance simulation
    p.stepSimulation()

    if i % 100 == 0:
        print(f"Step {i} | Dist: {distance:.2f}m | Heading Error: {heading_error:.2f} rad")

    time.sleep(1./240.)

if not reached:
    print("Mission timeout. Target not reached.")

print("Simulation ended and resources released.")