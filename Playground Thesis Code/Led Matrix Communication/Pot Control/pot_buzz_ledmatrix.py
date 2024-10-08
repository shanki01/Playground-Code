from machine import Pin, SoftI2C, PWM, ADC
from files import *
import time
import machine
from Tufts_ble import Sniff, Yell
import ledmatrix
import ssd1306
import sensors
import oledicons as pics

sens=sensors.SENSORS()
s = Pin(2, Pin.OUT)

def vibrate(delay=0.2):
    s.value(1)
    time.sleep(delay)
    s.value(0)

NAME_FLAG = 0x09
IRQ_SCAN_RESULT = 5
IRQ_SCAN_DONE = 6

i2c = SoftI2C(scl=Pin(7), sda=Pin(6))
a = ledmatrix.LEDMATRIX(i2c)
global oled
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

btn_send = Pin(9,Pin.IN, Pin.PULL_UP)

available_images = [ 'Smile', 'Sad', 'Heart', 'House', 'Tree', 'Flower', 'Crab', 'Duck', 'Cat']
image_nums = [0,2,10,20,21,22,26,27,29]
funs = [pics.draw_smiley, pics.draw_sad_face, pics.draw_heart, pics.draw_house,pics.draw_tree,pics.draw_flower, pics.draw_crab,pics.draw_duck,pics.draw_cat]

oled.fill(0)

def btn_send_callback(change):
    global advertisement
    global available_images
    global count
    print('send')
    advertisement = '!' + available_images[count]

global advertisement
advertisement = "!QMark"
p = Yell()

btn_send.irq(handler=btn_send_callback, trigger=Pin.IRQ_FALLING)  #start interrupt

c = Sniff('?', verbose = False)
c.scan(0)   # 0ms = scans forever

storedPic = '?QMark'
oldpos = 0
count = 1
display = funs[count]
display()

while True:
    pos = sens.readpot()
    diff = pos-oldpos
    if abs(diff) > 455:
        vibrate()
        if diff < 0:
            count += 1
        else:
            count -= 1
        print(count)
        display = funs[count]
        display()
        oldpos = pos
    p.advertise(advertisement)
    if c.last and c.last != storedPic:  
        storedPic = c.last[1:]
        emoji = image_nums[available_images.index(storedPic)]
        a.display_emoji(emoji,1,1)
        
