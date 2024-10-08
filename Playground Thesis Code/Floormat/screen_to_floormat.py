import time
from machine import Pin, ADC
import machine
import neopixel
import math
import Images_Library as pics
from Tufts_ble import Sniff, Yell
import random

NAME_FLAG = 0x09
IRQ_SCAN_RESULT = 5
IRQ_SCAN_DONE = 6

# Configure the LED strip
pin = machine.Pin(28)
num_leds = 256  # for a 9 by 15 matrix

strip = neopixel.NeoPixel(pin, num_leds)

def clear():
    strip.fill((0, 0, 0))
    strip.write()

def set_led(index, color):
    strip[index] = color
    strip.write()

def set_leds(indices, color):
    for index in indices:
        strip[index] = color
    strip.write()
    
intensity = .05  ### Change this value for brighter lights
available_images = [ 'Heart', 'Crab', 'Star', 'Crown', 'Rocket', 'X', 'O_Mark', 'Cactus', 'Happy', 'Sad', 'QMark']

storedPic = None
c = Sniff('!', verbose = False)
c.scan(0)   # 0ms = scans forever
storedPic = 'QMark'

while True:
    if c.last and c.last != storedPic:  
        pics.Images_16x16.clear()
        storedPic = c.last[1:]
        getattr(pics.Images_16x16, storedPic)()
        print(storedPic)
        time.sleep(2)
    time.sleep(0.5)
