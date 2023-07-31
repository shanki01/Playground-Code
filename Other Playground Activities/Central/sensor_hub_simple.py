#Code for hub acting as central with a sensor sending info to peripheral actuator hub
import bluetooth
import time
import ble_CBR
from central_functions import central
from hub import port
import force_sensor

device = central()

while True:
    device.connect()
    connected = device.is_connected()
    if connected:
        print('got here')
        while connected:
            connected = device.is_connected()
            pressed = force_sensor.is_pressed(port.A)
            if pressed:
                device.send('Pressed')
            time.sleep(0.5)
    time.sleep(2)
