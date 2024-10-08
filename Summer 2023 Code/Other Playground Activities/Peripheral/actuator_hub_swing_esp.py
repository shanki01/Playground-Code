#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_CBR
from peripheral_functions import peripheral
from machine import Pin
#import hub as spike
#import motor

device = peripheral()
led_1 = Pin(8, Pin.OUT)
led_2 = Pin(2, Pin.OUT)
led_1.value(0)
led_2.value(0)

def on_rx(v):
    parse = v.decode('ASCII')
    message = parse.replace('_', '')
    print("RX",message)
    if message == 'GREEN':
        print('lights green')
        led_2.value(0)
        led_1.value(1)
    if message == 'RED':
        print('lights red')
        led_1.value(0)
        led_2.value(1)

device.on_notify(on_rx)

while True:
    connected = device.is_connected()
    if connected:
        time.sleep(2)           
    else:
        time.sleep(2)
        device.on_notify(on_rx)
        time.sleep(2)
