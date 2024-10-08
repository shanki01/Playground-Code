import time
import sensors
from machine import Pin, ADC, SoftI2C
import machine
from Tufts_ble import Sniff, Yell
import ledmatrix
import ssd1306
import accel_tap

NAME_FLAG = 0x09
IRQ_SCAN_RESULT = 5
IRQ_SCAN_DONE = 6

i2c = SoftI2C(scl=Pin(7), sda=Pin(6))
a = ledmatrix.LEDMATRIX(i2c)
global oled
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
sensor = accel_tap.ADXL345(i2c)

# Enable single-tap detection
sensor.set_tap_threshold(50)  # Adjust the threshold (sensitivity)
sensor.set_tap_duration(15)   # Adjust tap duration for better responsiveness

# Enable the tap detection interrupt on axis
sensor.enable_tap_detection(single_tap=True, double_tap=False)

available_images = [ 'Smile', 'Sad', 'Heart', 'House', 'Tree', 'Flower', 'Crab', 'Duck', 'Cat']
image_nums = [0,2,10,20,21,22,26,27,29]

oled.fill(0)

def btn_up_callback():
    global count
    global oled
    print('change')
    oled.fill(0)
    if count < (len(available_images)-1):
        count += 1
    else:
        count = 0

global count
count = 0

storedPic = 'Smile'

while True:
    if sensor.is_tapped():
        btn_up_callback()
    global count
    storedPic = available_images[count]
    oled.text(storedPic, 0,0)
    oled.show()
    emoji = image_nums[count]
    a.display_emoji(emoji,1,1)
    time.sleep(0.5)