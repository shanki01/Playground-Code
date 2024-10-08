#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_CBR
from peripheral_functions import peripheral
import hub as spike
import motor

device = peripheral()
spike.light.color(0,9)

def on_rx(v):
    parse = v.decode('ASCII')
    message = parse.replace('_', '')
    print("RX",message)
    if message == 'Start':
        spike.light.color(0,5)
        On = True
        tic = time.ticks_ms()
        while On:
            if spike.button.pressed(0) > 0:
                spike.light.color(0,9)
                toc = time.ticks_ms()
                elapsed = (toc-tic)/1000
                print(elapsed)
                spike.light_matrix.write("You took" + str("%.2f" % elapsed) + "seconds")
                device.send('End')
                time.sleep(0.5)
                On = False
                
            
device.on_notify(on_rx)

while True:
    connected = device.is_connected()
    if connected:
        time.sleep(2)           
    else:
        time.sleep(2)
        device.on_notify(on_rx)
        time.sleep(2)
