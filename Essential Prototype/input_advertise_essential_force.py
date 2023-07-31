#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_CBR_short
from peripheral_functions_short import peripheral
from hub import port
from SensorFunctions import get_distance

hub.led(9) #red
count = 0
    
while True:
    try: 
        pressed = get_distance('A')
        if pressed > 0:
            value = True
        else:
            value = False
        if value:
            count += 1
            advertisement = 'force' + ',' + str(count)
            signal = peripheral(advertisement)
            signal.advertise()
            if count == 2:
                count = 0
            time.sleep(1)
    except Exception as e:
        print(e)
        port_searching = True
        break
