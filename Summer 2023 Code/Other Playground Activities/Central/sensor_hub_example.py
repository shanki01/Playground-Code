#Can turn connection on and off by pressing the center hub button
import bluetooth
import time
import ble_CBR
from central_functions import central
import hub as spike
import force_sensor

def on_rx(v):
    message = str(bytes(v))
    print("RX",message)
    if message == b'Disconnect':
        print('disconnecting')
        device.disconnect()
     
while True:
    spike.light.color(0,1)
    if spike.button.pressed(0) > 0:
        spike.light.color(0,5)
        device = central()
        device.on_notify(on_rx)
        while True:
            connected = device.is_connected()
            if connected:
                break
            else:
                device = central()
                device.on_notify(on_rx)
        while connected:
            connected = device.is_connected()
            force = force_sensor.is_pressed(spike.port.A)
            if force == 1:
                device.send('Pressed')
            if spike.button.pressed(0) > 0:
                print('disconnect')
                device.disconnect()
            time.sleep(0.1)
