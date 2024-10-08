import bluetooth
import time
import ble_CBR_short
from peripheral_functions_short import peripheral
from quick_scan import QuickScan
from hub import port
from SensorFunctions import get_distance

hub.led(6) #green - distance
motor = hub.port.B.motor
motor.preset(0)
inputs = ['dist','photo','force']
count_1 = 0
count = 0
green = 0
yellow = 45
red = 90
colors = [green,yellow,red]
color_count = 1
old_count = 0

def is_pressed(port):
    pressed = get_distance(port)
    if pressed > 0:
        return True
    else:
        return False
        
while True:
    try: 
        if is_pressed('A'):
            color_count += 1
            if color_count > 3:
                color_count = 1
        motor.run_to_position(colors[color_count - 1])
        input = inputs[color_count-1]
        if old_count != color_count:
            advertisement = 'lgt' + ',' + str(count) + ',' + str(color_count-1)
            per = peripheral(advertisement)
            per.advertise()
        old_count = color_count    
        
        central = QuickScan(input)  
        central.scan(0)   
        central.wait_for_scan()
    
        if central.peripheral != '' and central.peripheral != None:
            commands = central.peripheral.split(',')
            count = commands[1]
            if count != count_1:
                advertisement = 'lgt' + ',' + commands[1] + ',' + str(color_count-1)
                per = peripheral(advertisement)
                per.advertise()
                count_1 = count
        time.sleep(0.01)
    except Exception as e:
        print(e)
        port_searching = True
        break
    time.sleep(0.01)
