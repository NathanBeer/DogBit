import pybullet as p

robot_id = None

def set_robot_id(id):
    global robot_id
    robot_id = id

def move_x(speed):
    # Reduced speed to prevent the robot from flying off-screen
    p.resetBaseVelocity(robot_id, linearVelocity=[speed/100.0, 0, 0])

def turn(speed):
    # Control turn speed
    p.resetBaseVelocity(robot_id, angularVelocity=[0, 0, speed/50.0])

def stop():
    p.resetBaseVelocity(robot_id, [0, 0, 0], [0, 0, 0])