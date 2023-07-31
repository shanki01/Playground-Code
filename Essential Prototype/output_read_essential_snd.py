import bluetooth
import time
from quick_scan import QuickScan
from ble_advertising import decode_services, decode_name
import hub

count_1 = 0
green = 6
yellow = 7
red = 9
colors = [green, yellow, red]
hub.light_matrix.write('S')
  
while True: 
    try:  
        central = QuickScan('snd') 
        central.scan(0)
        central.wait_for_scan()
        if central.peripheral != '' and central.peripheral != None:
            commands = central.peripheral.split(',')
            count = commands[1]
            color = colors[int(commands[2])]
            hub.light.color(0,color)
            if count != count_1:
                hub.speaker.beep(1000,400,100)
                count_1 = count       
        time.sleep(0.01)
    except Exception as e:
        print(e)
        port_searching = True
        break
        
        