#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_CBR
from peripheral_functions import peripheral
from hub import port
import motor

device = peripheral()

def on_rx(v):
    parse = v.decode()
    message = parse.replace('_', '')
    print("RX",message)
    device.send(message)

device.on_notify(on_rx)

while True:
    connected = device.is_connected()
    if connected:
        time.sleep(2)           
    else:
        time.sleep(2)
        device.on_notify(on_rx)
        time.sleep(2)
