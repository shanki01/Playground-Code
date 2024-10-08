import time
from machine import Pin, ADC, SoftI2C
import machine
from Tufts_ble import Sniff, Yell
import ledmatrix
import ssd1306

NAME_FLAG = 0x09
IRQ_SCAN_RESULT = 5
IRQ_SCAN_DONE = 6

i2c = SoftI2C(scl=Pin(7), sda=Pin(6))
a = ledmatrix.LEDMATRIX(i2c)
global oled
oled = ssd1306.SSD1306_I2C(128, 64, i2c)


available_images = [ 'Smile', 'Sad', 'Heart', 'House', 'Tree', 'Flower', 'Crab', 'Duck', 'Cat']
image_nums = [0,2,10,20,21,22,26,27,29]

oled.fill(0)
btn_up = Pin(10,Pin.IN, Pin.PULL_UP)
btn_send = Pin(9,Pin.IN, Pin.PULL_UP)

def btn_up_callback(change):
    global count
    global oled
    print('change')
    oled.fill(0)
    if count < len(available_images):
        count += 1
    else:
        count = 0

def btn_send_callback(change):
    global advertisement
    global available_images
    global count
    print('send')
    advertisement = '!' + available_images[count]

global advertisement
advertisement = "!QMark"
p = Yell()

global count
count = 0
btn_up.irq(handler=btn_up_callback, trigger=Pin.IRQ_FALLING)  #start interrupt
btn_send.irq(handler=btn_send_callback, trigger=Pin.IRQ_FALLING)  #start interrupt

storedPic = None
c = Sniff('?', verbose = False)
c.scan(0)   # 0ms = scans forever
storedPic = '?QMark'

while True:
    global count
    oled.text(available_images[count], 0,0)
    oled.show()
    p.advertise(advertisement)
    if c.last and c.last != storedPic:  
        storedPic = c.last[1:]
        emoji = image_nums[available_images.index(storedPic)]
        a.display_emoji(emoji,1,1)
    time.sleep(0.5)