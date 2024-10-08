#Code for hub acting as central with a sensor sending info to peripheral actuator hub
import bluetooth
import time
import ble_CBR
from central_functions import central
import hub as spike
import distance_sensor

while True:
    device = central()
    count = 0
    try:
        connected = device.is_connected()
        if connected:
            while connected:
                connected = device.is_connected()
                distance = distance_sensor.distance(spike.port.A)
                if distance > 0 and distance < 1000:
                    count += 1
                    if count % 2 == 0:
                        device.send('GREEN')
                        time.sleep(1)
                    else:
                        device.send('RED')
                        time.sleep(1)
                time.sleep(0.1)
    except:
        time.sleep(2)
