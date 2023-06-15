#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_CBR
from peripheral_functions import peripheral
import hub as spike
import motor

signal = peripheral()
device = signal.hub
spike.light.color(0,0)

def on_rx(v):
    parse = v.decode('ASCII')
    message = parse.replace('_', '')
    print("RX",message)
    if message == 'GREEN':
        spike.light.color(0,5)
    if message == 'RED':
        spike.light.color(0,9)

device.on_write(on_rx)

while True:
    connected = device.is_connected()
    if connected:
        time.sleep(2)           
    else:
        time.sleep(2)
        device.on_write(on_rx)
        time.sleep(2)
