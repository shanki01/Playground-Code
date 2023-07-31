#Code for hub acting as central with a sensor sending info to peripheral actuator hub
import bluetooth
import time
import ble_CBR
from central_functions import central
import hub as spike
import force_sensor

spike.light.color(0,9)
spike.light_matrix.clear()

def on_rx_1(v):
    parse = bytes(v).decode('ASCII')
    message = parse.replace('_','')
    print("RX",message)
    if message == 'Pressed':
        device.flag = True
    else:
        device.flag = False
        
while True:
    device = central()
    try:
        connected = device.is_connected()
        if connected:
            while connected:
                switch = False
                connected = device.is_connected()
                device.on_notify(on_rx_1)
                pressed = force_sensor.is_pressed(spike.port.B)
                while pressed:
                    switch = True
                    spike.light.color(0,5)
                    pressed = force_sensor.is_pressed(spike.port.B)
                    device.send('Pressed')
                    while signal.flag and pressed:
                        spike.light.color(0,1)
                        spike.light_matrix.show_image(3)
                        pressed = force_sensor.is_pressed(spike.port.B)
                        device.send('Pressed')
                    spike.light_matrix.clear()
                    time.sleep(0.2)
                spike.light.color(0,9)
                spike.light_matrix.clear()
                if switch:
                    device.send('Not Pressed')
                time.sleep(0.1) 
            time.sleep(0.1)
                
    except:
        time.sleep(2)
