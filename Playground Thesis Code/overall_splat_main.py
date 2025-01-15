import time
import struct
from networking import Networking
from machine import Pin, SoftI2C, PWM, ADC
from splat import Splat

s = Splat('1')
s.set_color()
    
while True:
    if s.is_pressed():
        s.send_to_close_modules()
        #s.play_sound()
    time.sleep(0.5)