#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_SMH
from peripheral_functions_short import peripheral
from machine import ADC, Pin

count = 0
photo = Pin(2)
light = Pin(4,Pin.OUT)
light.value(1)

while True:
    try: 
        raw = photo.value()
        if raw == 0:
            value = True
        else:
            value = False
        if value:
            count += 1
            advertisement = 'photo' + ',' + str(count)
            print(advertisement)
            signal = peripheral(advertisement)
            signal.advertise()
            if count == 2:
                count = 0
            time.sleep(2)
        time.sleep(0.2)
    except Exception as e:
        print(e)
        break
