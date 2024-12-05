import bluetooth
import time
import struct
from networking import Networking
from led_sequence import LEDSequencer
import ledmatrix
import ssd1306
import sensors
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
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'cyan', 'purple','pink']
sent_sequence = []
last_num = None
num = None

networking = Networking(True, False) #First bool is for network info messages, second for network debug messages
broadcast_mac = b'\xff\xff\xff\xff\xff\xff'
networking.aen.add_peer(broadcast_mac, "All")
networking.name = 'observer'

def receive():
    try:
        for mac, message, rtime in networking.aen.return_messages(): #You can directly iterate over the function
            global count, x, y, repeat, last_num, sent_sequence, num, matches
            if len(message) < 4 and repeat:
                if count < 4:
                    num = int(message)
                    if num != last_num and num != None:
                        color = colors[num-1]
                        for i in range (0,2):
                            sequencer.display_color_pixel(color, x-i, y)
                        check_buffer()
                        if matches:
                            x = x-2
                            count += 1
                            last_num = num
                            target_num = sent_sequence[count]
                            sequencer.display_number(target_num,colors[target_num-1])
                        else:
                            time.sleep(0.5)
                            for i in range (0,2):
                                sequencer.display_color_pixel('black', x-i, y)
            else:
                sequencer.clear_display()
                sent_sequence = message
                for i in range(0,len(sent_sequence)):
                    color = colors[sent_sequence[i]-1]
                    sequencer.display_color_pixel(color,7-2*i,7)
                    sequencer.display_color_pixel(color,7-(2*i+1),7)
                repeat = True
                count = 0
                x = 7
                y = 6
                target_num = sent_sequence[count]
                sequencer.display_number(target_num,colors[target_num-1])
                
    except Exception as e:
        print(e)
        
def check_buffer():
    global num, matches, count, sent_sequence
    if num != sent_sequence[count]: #scanned wrong beacon
        vibrate()
        progress = sequencer.buffer[48:56]
        sequencer.buffer[48:56] = [0]*8
        matrix.display_frames(sequencer.buffer, 1000,1,1)
        time.sleep(0.5)
        sequencer.buffer[48:56] = progress
        matrix.display_frames(sequencer.buffer, 1000,1,1)
        matches = False
    else:
        matches = True
        
networking.aen.irq(receive)
color = None
x = 7
y = 6
count = 0

while True:
    if count > 3:
        buffer = [0x52]*64
        matrix.display_frames(buffer, 1000,1,1)
        repeat = False
    time.sleep(0.05)


