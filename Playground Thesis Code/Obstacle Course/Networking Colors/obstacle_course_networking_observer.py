import bluetooth
import time
import struct
from networking import Networking
from led_sequence import LEDSequencer
import ledmatrix
import ssd1306
import sensors
#from variableLED import VariableLED
#from rssi_ble import Yell, Sniff
from machine import Pin, SoftI2C, PWM, ADC

#oled screen
i2c = SoftI2C(scl = Pin(7), sda = Pin(6)) # Adjust the pins if necessary
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)

#haptic motor
sens=sensors.SENSORS()
s = Pin(2, Pin.OUT)

def vibrate(delay=0.2):
    s.value(1)
    time.sleep(delay)
    s.value(0)

#LED Matrix
matrix = ledmatrix.LEDMATRIX(i2c)
sequencer = LEDSequencer(matrix)
sequencer.clear_display()

repeat = False
buffer = [255] *64
matches = True

networking = Networking(True, False) #First bool is for network info messages, second for network debug messages
broadcast_mac = b'\xff\xff\xff\xff\xff\xff'
networking.aen.add_peer(broadcast_mac, "All")
networking.name = 'observer'
            
switch_select = Pin(9, Pin.IN, Pin.PULL_UP)

def receive():
    try:
        for mac, message, rtime in networking.aen.return_messages(): #You can directly iterate over the function
            global buffer, count, x, y
            buffer = [255] *64
            buffer[0:len(message)] = message
            sequencer.buffer = buffer
            matrix.display_frames(buffer, 1000,1,1)
            global repeat
            repeat = True
            count = 0
            x = 7
            y = 3
    except Exception as e:
        print(e)
        
def check_buffer():
    for i in range(0,8):
        global buffer
        pixel = buffer[31-i]
        global matches
        if pixel != 255 and pixel != buffer[7-i]: #scanned wrong beacon
            vibrate()
            buffer[-8:] = [0]*8
            matrix.display_frames(buffer, 1000,1,1)
            time.sleep(1)
            buffer[-8:] = [255]*8
            buffer[31-i] = 255
            matrix.display_frames(buffer, 1000,1,1)
            matches = False
            break
        matches = True
        
networking.aen.irq(receive)
color = None
last_name = None
x = 7
y = 3
count = 0

while True:
    if repeat:
        if count < 8:
            for key in networking.aen.rssi():
                if networking.aen.rssi()[key][0] > -25:
                    color = networking.aen.peer_name(key)
            if color != last_name:
                print(color)
                sequencer.display_color_pixel(color, x, y)
                check_buffer()
                if matches:
                    x -= 1
                    last_name = color
                    count += 1
        else:
            buffer = [0x52]*64
            matrix.display_frames(buffer, 1000,1,1)
            repeat = False
        time.sleep(0.05)


