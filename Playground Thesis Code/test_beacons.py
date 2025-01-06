import bluetooth
import time
import struct
from networking import Networking
import sensors
from variableLED import VariableLED
from machine import Pin, SoftI2C, PWM, ADC

#variable LED
pin_clk = Pin(7, Pin.OUT)
pin_data = Pin(6, Pin.OUT)
num_leds = 1
color = VariableLED(pin_clk, pin_data, num_leds)
color[0] = (255,0,0)  #Change color for each board
color.write()

def send(pin):
    global broadcast_mac
    rssi_buffer = []
    key_buffer = []
    networking.aen.ping(broadcast_mac)
    time.sleep(0.1)
    print(networking.aen.rssi())
    for key in networking.aen.rssi():
        rssi = networking.aen.rssi()[key][0]
        if rssi > -25:
            networking.aen.send(key, '1')

networking = Networking(True, False) #First bool is for network info messages, second for network debug messages
broadcast_mac = b'\xff\xff\xff\xff\xff\xff'
networking.aen.add_peer(broadcast_mac, "All")
networking.aen.ping(broadcast_mac)
            
switch_select = Pin(9, Pin.IN, Pin.PULL_UP)
switch_select.irq(trigger=Pin.IRQ_FALLING, handler=send)

while True:
    time.sleep(1)
