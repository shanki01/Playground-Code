import time
import struct
from networking import Networking
import ledmatrix
import ssd1306
import sensors
import icons
from module import Module
from machine import Pin, SoftI2C, PWM, ADC, Timer

module = Module()

batt = Timer(2)
batt.init(period=1000, mode=Timer.PERIODIC, callback=module.displaybatt)

while True:
    module.display_correct()
    time.sleep(1)
    module.send(module.broadcast_mac,'hello')
    module.display_wrong()
    module.networking.aen.ping(module.broadcast_mac)
    time.sleep(0.5)
    