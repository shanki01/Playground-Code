import bluetooth
import time
import struct
from networking import Networking
from led_sequence import LEDSequencer
import ledmatrix
import ssd1306
import sensors
from variableLED import VariableLED
from rssi_ble import Yell, Sniff
from machine import Pin, SoftI2C, PWM, ADC

'''
#variable LED
pin_clk = Pin(7, Pin.OUT)
pin_data = Pin(6, Pin.OUT)
num_leds = 1
color = VariableLED(pin_clk, pin_data, num_leds)
'''

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
espnow = False


def send(pin):
    global broadcast_mac, y
    networking.aen.send(broadcast_mac, sequencer.buffer[0:8*(y+1)])

networking = Networking(True, False) #First bool is for network info messages, second for network debug messages
broadcast_mac = b'\xff\xff\xff\xff\xff\xff'
networking.aen.add_peer(broadcast_mac, "All")
            
switch_select = Pin(9, Pin.IN, Pin.PULL_UP)
switch_select.irq(trigger=Pin.IRQ_FALLING, handler=send)

color = None
last_name = None
x = 7
y = 0
count = 0

try:
    while count < 8:
        for key in networking.aen.rssi():
            if networking.aen.rssi()[key][0] > -25:
                color = networking.aen.peer_name(key)
        if color != last_name:
            print(color)
            sequencer.display_color_pixel(color, x, y)
            if x == 0:
                y += 1
                x = 7
            else:
                x -= 1
            last_name = color
            count += 1
        time.sleep(0.05)

except Exception as e:
    print(e)
