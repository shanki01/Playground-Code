import bluetooth
import time
from quick_scan import QuickScan
from ble_advertising import decode_services, decode_name
import hub
import motor

count_1 = 0
green = 6
yellow = 7
red = 9
colors = [green, yellow, red]   
hub.light_matrix.write('M')

while True: 
    try:  
        central = QuickScan('mtr') 
        central.scan(0)
        central.wait_for_scan()
        if central.peripheral != '' and central.peripheral != None:
            commands = central.peripheral.split(',')
            count = commands[1]
            color = colors[int(commands[2])]
            hub.light.color(0,color)
            if count != count_1:
                motor.run(hub.port.A,1000)
                time.sleep(0.5)
                motor.run(hub.port.A,0)
                count_1 = count       
        time.sleep(0.01)
    except Exception as e:
        print(e)
        port_searching = True
        break
        