#Code for hub acting as central with a sensor sending info to peripheral actuator hub
import bluetooth
import time
import ble_CBR
from central_functions import central
import hub as spike

spike.light.color(0,9)

def on_rx(v):
    message = str(bytes(v))
    print("RX",message)
    spike.light.color(0,9)
        
while True:
    device = central()
    count = 0
    try:
        connected = device.is_connected()
        if connected:
            while connected:
                connected = device.is_connected()
                if spike.button.pressed(0) > 0:
                    spike.light.color(0,5)
                    device.send('Start')
                    device.on_notify(on_rx)
                time.sleep(0.1)
    except:
        time.sleep(2)
