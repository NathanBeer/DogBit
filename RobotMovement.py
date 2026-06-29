import platform

class BluetoothController:
    def __init__(self):
        # Detect if we are on a Raspberry Pi
        self.is_pi = platform.machine().startswith('arm')
        if self.is_pi:
            from BluetoothWorker import BluetoothController as ActualController
            self.controller = ActualController()
        else:
            self.controller = None
            print("[Mock] Bluetooth hardware disabled (Not on Pi).")

    def send(self, packet):
        if self.controller:
            self.controller.send(packet)
        else:
            print(f"[Mock] Sent packet: {packet}")

controller = BluetoothController()

def rotate(speed=30, direction="right"):
    val = 0x01 if direction == "right" else 0x02
    controller.send([0x55, 0x00, 0x09, val, speed])

def move_forward(speed=50):
    controller.send([0x55, 0x00, 0x09, 0x03, speed])

def safe_stop():
    controller.send([0x55, 0x00, 0x09, 0x00, 0x00])