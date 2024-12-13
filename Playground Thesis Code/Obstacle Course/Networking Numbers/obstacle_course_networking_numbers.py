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

#oled screen
i2c = SoftI2C(scl = Pin(7), sda = Pin(6)) # Adjust the pins if necessary
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)


#LED Matrix
matrix = ledmatrix.LEDMATRIX(i2c)
sequencer = LEDSequencer(matrix)
sequencer.clear_display()

def send(pin):
    global broadcast_mac
    networking.aen.send(broadcast_mac, sequence)

networking = Networking(True, False) #First bool is for network info messages, second for network debug messages
broadcast_mac = b'\xff\xff\xff\xff\xff\xff'
networking.aen.add_peer(broadcast_mac, "All")
            
switch_select = Pin(9, Pin.IN, Pin.PULL_UP)
switch_select.irq(trigger=Pin.IRQ_FALLING, handler=send)

last_num = None
x = 7
y = 7
count = 0
sequence = []
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'cyan', 'purple','pink']

def receive():
    for mac, message, rtime in networking.aen.return_messages():
        global count, sequence, last_num
        if count < 4 and last_num != int(message):
            sequence.append(int(message))
            print(sequence)
            
networking.aen.irq(receive)

try:
    while True:
        if len(sequence) != 0:
            num = sequence[-1]
            color = colors[num-1]
            if num != last_num and num != None:
                sequencer.display_number(num,color)
                for i in range (0,2):
                    sequencer.display_color_pixel(color, x-i, y)
                x = x-2
                last_num = num
                count += 1
        time.sleep(0.05)

except Exception as e:
    print('error:', e)
