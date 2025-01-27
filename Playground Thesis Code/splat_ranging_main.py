import time
import struct
from machine import Pin, SoftI2C, PWM, ADC
from splat2 import Splat

s = Splat('5')
s.set_color()

def callback(pin):
    time.sleep(0.001)
    if not pin.value():
        s.is_pressed = True

s.sw1.irq(trigger=Pin.IRQ_RISING, handler=callback)
s.sw2.irq(trigger=Pin.IRQ_RISING, handler=callback)
s.sw3.irq(trigger=Pin.IRQ_RISING, handler=callback)
s.sw4.irq(trigger=Pin.IRQ_RISING, handler=callback)
    
while True:
    s.send_to_close_modules()
    '''
    if s.is_pressed:
        s.send_to_close_modules()
        s.play_sound()
        s.is_pressed = False
        '''
    time.sleep(0.5)