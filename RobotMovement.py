from gpiozero import Robot
from time import sleep

# Define the pins connected to your motor driver
# Example: Left motor on pins 17/18, Right motor on 22/23
dog_robot = Robot(left=(17, 18), right=(22, 23))

def move_forward():
    print("[Movement] Moving forward")
    dog_robot.forward(speed=0.5) # Speed from 0.0 to 1.0

def stop():
    print("[Movement] Stopping")
    dog_robot.stop()

def turn_left():
    print("[Movement] Turning left")
    dog_robot.left(speed=0.4)

def turn_right():
    print("[Movement] Turning right")
    dog_robot.right(speed=0.4)