import sys
sys.coinit_flags = 0  # חובה גם כאן כדי להגן על התהליך החדש בווינדוס!

import asyncio
from bleak import BleakClient
import multiprocessing

MAC_ADDRESS = "C4:D8:D5:A5:D2:82"
CHAR_UUID = "0000fff2-0000-1000-8000-00805f9b34fb" 

# ... המשך הקוד של run_ble_worker ו-BluetoothController נשאר זהה ... 

def run_ble_worker(command_queue):
    async def main():
        async with BleakClient(MAC_ADDRESS) as client:
            print("[Bluetooth] Worker connected!")
            while True:
                # מחכה לפקודה מהקוד הראשי
                cmd = command_queue.get()
                if cmd is None: break # אות סגירה
                await client.write_gatt_char(CHAR_UUID, cmd)
    
    asyncio.run(main())

class BluetoothController:
    def __init__(self):
        self.queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=run_ble_worker, args=(self.queue,))
        self.process.start()
        
    def send(self, data):
        self.queue.put(bytearray(data))