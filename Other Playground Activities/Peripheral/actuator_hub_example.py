#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_CBR
from peripheral_functions import peripheral
import hub as spike
import motor


def on_rx(v):
    parse = v.decode('ASCII')
    message = parse.replace('_', '')
    print("RX",message)
    if message == 'Pressed':
        motor.run(spike.port.A,1000)
        time.sleep(0.5)
        motor.run(spike.port.A,0)
        pos = motor.relative_position(spike.port.A)
        device.send(str(pos))

while True:
    spike.light.color(0,1)
    if spike.button.pressed(0) > 0:
        spike.light.color(0,5)
        device = peripheral()
        device.on_notify(on_rx)
        while True:
            connected = device.is_connected()
            if connected:
                break
        while connected:
            connected = device.is_connected()
            if spike.button.pressed(0) > 0:
                device.send('Disconnect')
                print('disconnect')
                device.disconnect()
            time.sleep(0.1)    