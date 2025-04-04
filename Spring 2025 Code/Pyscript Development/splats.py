from pyscript import window
from pyscript.js_modules import ble
import struct

SERVICE_UUID = '0000fff0-0000-1000-8000-00805f9b34fb'
WRITE_UUID   = '0000fff3-0000-1000-8000-00805f9b34fb'
NOTIFY_UUID  = '0000fff4-0000-1000-8000-00805f9b34fb'

class Hub():
    def __init__(self):
        self.info = None
        self.myble = ble.myBLE

    def callback(self, callback):
        self.myble.callback = callback

    async def connect(self, name):
        await self.myble.connect(name, SERVICE_UUID, WRITE_UUID, NOTIFY_UUID)
        #await self.write([0x00, 0x10]) # confirm connection

    def disconnect(self):
        self.myble.disconnect()

    async def write(self, data):
        await self.myble.write(data)

    def parse(self, data):
        yaw = data[2]
        #yaw = ((data[1] << 8) | data[0]) & 0x3FF
        #yaw = struct.unpack('<h',bytes(data[0:2]))[0]
        #yaw = struct.unpack('<h',data)[0]
        #window.console.log('yaw ',yaw)
        return yaw
