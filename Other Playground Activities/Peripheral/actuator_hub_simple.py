#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_CBR
from peripheral_functions import peripheral
from hub import port
import motor

device = peripheral()
advertising = False

def on_rx(v):
    parse = v.decode('ASCII')
    message = parse.replace('_', '')
    print("RX",message)
    if message == 'Pressed':
        motor.run(port.A,1000)
        time.sleep(0.5)
        motor.run(port.A,0)
        pos = motor.relative_position(port.A)
        device.send(str(pos))


while True:
    if not advertising:
        device.advertise()
        advertising = True
    device.on_notify(on_rx)
    connected = device.is_connected()
    while connected:
        connected = device.is_connected()
        advertising = False
        time.sleep(2)
    time.sleep(2)