import bluetooth
import time
import ble_SMH
from peripheral_functions_short import peripheral
from quick_scan import QuickScan
from ble_advertising import decode_services, decode_name
from machine import ADC, Pin
import machine
from variable_led import VariableLED

pin_clk = Pin(2, Pin.OUT)
pin_data = Pin(3, Pin.OUT)
num_leds = 1
color = VariableLED(pin_clk, pin_data, num_leds)
color_button = Pin(4, Pin.IN, Pin.PULL_DOWN)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
colors = [red,green,blue]
global inputs
inputs = ['force','photo','dist']
input = inputs[0]
count_1 = 0
global color_count
color_count = 1
color[0] = colors[color_count - 1]
color.write()
global old_count
old_count = 0
global count
count = 0
per = peripheral('ESP')
        
def color_change(pin):
    global color_count
    global old_count
    global count
    if color_button.value():
        color_count += 1
        if color_count > 3:
            color_count = 1
        color[0] = colors[color_count - 1]
        color.write()
        global input
        input = inputs[color_count - 1]
        central.target = input
        advertisement = 'snd' + ',' + str(count) + ',' + str(color_count-1)
        per.advertise(advertisement)
        old_count = color_count
    
color_button.irq(color_change)
central = QuickScan(input)
central.scan(0)

while True:
    try: 
        if central.peripheral != '' and central.peripheral != None:
            commands = central.peripheral.split(',')
            count = commands[1]
            if count_1 != count:
                advertisement = 'snd' + ',' + commands[1] + ',' + str(color_count-1)
                per.advertise(advertisement)
                count_1 = count
        time.sleep(0.02)
    except Exception as e:
        print(e)
        break
    time.sleep(0.01)