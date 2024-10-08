#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_CBR
from peripheral_functions import peripheral
import hub as spike
import force_sensor

device = peripheral()
spike.light.color(0,9)
spike.light_matrix.clear() 
switch = False

def on_rx_1(v):
    parse = v.decode('ASCII')
    message = parse.replace('_', '')
    print("RX",message)
    if message == 'Pressed':
        device.flag = True
    else:
        device.flag = False
                
while True:
    try:
        connected = device.is_connected()
        if connected:
            while connected:
                switch = False
                connected = device.is_connected()
                device.on_notify(on_rx_1)
                pressed = force_sensor.is_pressed(spike.port.A)
                while pressed:
                    switch = True
                    spike.light.color(0,5)
                    pressed = force_sensor.is_pressed(spike.port.A)
                    device.send('Pressed')
                    while signal.flag and pressed:
                        spike.light.color(0,1)
                        spike.light_matrix.show_image(3)
                        pressed = force_sensor.is_pressed(spike.port.A)
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
