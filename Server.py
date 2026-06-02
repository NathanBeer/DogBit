from dogzilla import forward, back, left, right, turnleft, turnright, stop

# ... inside your server loop where you receive the command:
if cmd == "FORWARD":
    forward(15)  # 15 is the "step width" (speed)
elif cmd == "BACK":
    back(15)
elif cmd == "LEFT":
    left(10)
elif cmd == "RIGHT":
    right(10)
elif cmd == "STOP":
    stop()