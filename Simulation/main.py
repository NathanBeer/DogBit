import pybullet as p
import pybullet_data
import time
import RobotMovement_Sim as RobotMovement
import RobotSeeing_Sim as RobotSeeing

# 1. Define the stabilization function inside main.py 
# (or import it from a utility file)
def stabilize_robot(robot_id):
    stand_pose = [0, 0.6, -1.2, 0, 0.6, -1.2, 0, 0.6, -1.2, 0, 0.6, -1.2]
    for i in range(12):
        p.resetJointState(robot_id, i, stand_pose[i])
        p.setJointMotorControl2(robot_id, i, p.POSITION_CONTROL, targetPosition=stand_pose[i], force=100)

def main():
    # 2. SETUP
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")
    
    # Define these variables inside the function so they are recognized
    robot_id = p.loadURDF("laikago/laikago.urdf", [0, 0, 0.4])
    ball_pos = [3, 2, 0.2]
    ball_id = p.createMultiBody(baseMass=0, 
                                baseVisualShapeIndex=p.createVisualShape(p.GEOM_SPHERE, radius=0.2), 
                                basePosition=ball_pos)
    
    # 3. INITIALIZATION
    stabilize_robot(robot_id)
    
    # 4. MISSION LOOP
    for step in range(10000):
        # Pass the variables explicitly to the functions
        pos_r = p.getBasePositionAndOrientation(robot_id)[0]
        
        # Navigation logic using the defined variables
        # RobotMovement.walk_towards(robot_id, ball_id) 
        
        p.stepSimulation()
        time.sleep(1./240.)

    p.disconnect()

if __name__ == "__main__":
    main()