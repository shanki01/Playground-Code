#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_CBR_short
from peripheral_functions_short import peripheral
from machine import ADC, Pin
from Ultrasonic_Sensor import GroveUltrasonicRanger

count = 0
distance_sensor = GroveUltrasonicRanger(2)

while True:
    try: 
        raw = distance_sensor.get_distance()
        if raw < 100:
            value = True
        else:
            value = False
        if value:
            count += 1
            advertisement = 'dist' + ',' + str(count)
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
