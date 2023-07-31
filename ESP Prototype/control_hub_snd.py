import bluetooth
import time
import ble_CBR_short
from peripheral_functions_short import peripheral
from quick_scan import QuickScan
from ble_advertising import decode_services, decode_name
from machine import ADC, Pin
import machine
from variable_led import VariableLED

pin_clk = Pin(7, Pin.OUT)
pin_data = Pin(6, Pin.OUT)
num_leds = 1
color = VariableLED(pin_clk, pin_data, num_leds)
mode_button = ADC(Pin(4))
color_button = ADC(Pin(3))
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
colors = [green,red,blue]
inputs = ['force','photo','dist']
count_1 = 0
mode_count = 0
color_count = 1

def is_pressed(button):
    raw = button.read_u16()
    if raw > 60000:
        return True
    else:
        return False

while True:
    while mode_count == 0:
        if is_pressed(mode_button):
            mode_count = 1
        if is_pressed(color_button):
            color_count += 1
            if color_count > 3:
                color_count = 1
        color[0] = colors[color_count - 1]
        color.write()
        input = inputs[color_count - 1]
        print(input)
        time.sleep(0.5)
        
    while True:
        try: 
            if is_pressed(mode_button):
                mode_count = 0
                break
                
            central = QuickScan(input)
            central.scan(1000)
            central.wait_for_scan()
            
            if central.peripheral != '':
                commands = central.peripheral.split(',')
                count = commands[1]
                if count_1 != count:
                    advertisement = 'snd' + ',' + commands[1] + ',' + str(color_count-1)
                    print(advertisement)
                    per = peripheral(advertisement)
                    per.advertise()
                    count_1 = count
                    time.sleep(0.5)
            time.sleep(1)
        except Exception as e:
            print(e)
            break
    time.sleep(0.5)
