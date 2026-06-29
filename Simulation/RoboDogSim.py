import pybullet as p
import pybullet_data
import time
import numpy as np
import random

# 1. SETUP
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# 2. LOAD & STABILIZE
start_pos = [0, 0, 0.4]
robot_id = p.loadURDF("laikago/laikago.urdf", start_pos)

# Force the robot into a standing pose
def stabilize_robot(robot_id):
    # Joint indices for legs
    joints = [1, 2, 4, 5, 7, 8, 10, 11]
    stand_pose = [0.6, -1.2, 0.6, -1.2, 0.6, -1.2, 0.6, -1.2]
    for i, j in enumerate(joints):
        p.resetJointState(robot_id, j, stand_pose[i])
        p.setJointMotorControl2(robot_id, j, p.POSITION_CONTROL, targetPosition=stand_pose[i], force=50)

stabilize_robot(robot_id)

# Let physics "settle" for 1 second
for _ in range(240):
    p.stepSimulation()
    time.sleep(1./240.)

# 3. SPAWN TARGET
target_pos = [random.uniform(2, 5), random.uniform(-2, 2), 0.2]
ball_visual = p.createVisualShape(p.GEOM_SPHERE, radius=0.2, rgbaColor=[1, 0, 0, 1])
ball_id = p.createMultiBody(baseMass=0, baseVisualShapeIndex=ball_visual, basePosition=target_pos)

# 4. YOUR GAIT CONTROLLER
def gait_step(robot_id, forward_speed, turn_speed, phase):
    joints = [1, 2, 4, 5, 7, 8, 10, 11]
    amplitude = 0.1 # Reduced for stability
    for i, j_idx in enumerate(joints):
        offset = phase + (i % 2) * np.pi
        target = amplitude * np.sin(offset) * forward_speed
        if j_idx in [3, 4, 5, 9, 10, 11]: target += turn_speed
        else: target -= turn_speed
        p.setJointMotorControl2(robot_id, j_idx, p.POSITION_CONTROL, targetPosition=target, force=10)

# 5. MAIN LOOP
phase = 0
for i in range(5000):
    # Camera follow
    pos, _ = p.getBasePositionAndOrientation(robot_id)
    p.resetDebugVisualizerCamera(2, 45, -30, pos)
    
    # Navigation Logic (Simplified)
    # [Insert your heading/distance logic here]
    
    gait_step(robot_id, 0.5, 0, phase)
    phase += 0.1
    p.stepSimulation()
    time.sleep(1./240.)