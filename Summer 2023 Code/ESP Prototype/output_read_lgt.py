import bluetooth
import time
from quick_scan import QuickScan
from ble_advertising import decode_services, decode_name
from machine import ADC, Pin
from variable_led import VariableLED

pin_clk = Pin(4, Pin.OUT)
pin_data = Pin(5, Pin.OUT)
num_leds = 1
color = VariableLED(pin_clk, pin_data, num_leds)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
colors = [red,green,blue]

light = Pin(2,Pin.OUT)
light.value(0)
count_1 = 0

central = QuickScan('lgt') 
central.scan(0)
  
while True: 
    try: 
        if central.peripheral != '' and central.peripheral != None:
            commands = central.peripheral.split(',')
            count = commands[1]
            color_count = int(commands[2])
            color[0] = colors[color_count]
            color.write()
            if count != count_1:
                light.value(1)
                time.sleep(2)
                light.value(0)
                count_1 = count       
        time.sleep(0.01)
    except Exception as e:
        print(e)
        break
