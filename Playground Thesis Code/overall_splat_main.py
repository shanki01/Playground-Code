import time
import struct
from networking import Networking
from machine import Pin, SoftI2C, PWM, ADC
from splat import Splat

s = Splat('1')
s.light_on()

def send(pin):
    s.send_to_close_modules()
    s.play_sound()
            
#change to splat triggers
switch_select = Pin(9, Pin.IN, Pin.PULL_UP)
switch_select.irq(trigger=Pin.IRQ_FALLING, handler=send)

while True:
    time.sleep(1)