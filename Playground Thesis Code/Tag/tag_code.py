import bluetooth
import time
import struct
import asyncio
import neopixel
import ssd1306
from machine import Pin, SoftI2C
from variableLED import VariableLED

pin_clk = Pin(7, Pin.OUT)
pin_data = Pin(6, Pin.OUT)
num_leds = 1
color = VariableLED(pin_clk, pin_data, num_leds)

i2c = SoftI2C(scl = Pin(7), sda = Pin(6)) # Adjust the pins if necessary
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)

NAME_FLAG = 0x09
IRQ_SCAN_RESULT = 5
IRQ_SCAN_DONE = 6

BRIGHTNESS = 10

'''led = neopixel.NeoPixel(Pin(28),1)
led[0] = (BRIGHTNESS,0,BRIGHTNESS)
led.write()'''

class Sniff: 
    def __init__(self, cutoff = -30): 
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        self.scanning = False 
        self.names = [0]*255 
        self.cutoff = cutoff

    def _irq(self, event, data):
        if event == IRQ_SCAN_RESULT: 
            addr_type, addr, adv_type, rssi, adv_data = data
            name = self.decode_name(adv_data)
            if len(name) > 1:
                if name[0] == '!':
                    i = ord(name[1])
                    print(i,rssi)
                    self.names[i]=int(rssi > self.cutoff)
  
        elif event == IRQ_SCAN_DONE:  # close everything
            self.scanning = False

    def decode_field(self, payload, adv_type):
        i = 0
        result = []
        while i + 1 < len(payload):
            if payload[i + 1] == adv_type:
                result.append(payload[i + 2 : i + payload[i] + 1])
            i += 1 + payload[i]
        return result
        
    def decode_name(self,payload):
        n = self.decode_field(payload, NAME_FLAG)
        return str(n[0], "utf-8") if n else ""

    def scan(self, duration = 2000):
        self.scanning = True
        #run for duration sec, with checking every 30 ms for 30 ms
        duration = 0 if duration < 0 else duration
        return self._ble.gap_scan(duration, 3000, 3000)

    def stop_scan(self):
        self._scan_callback = None
        self._ble.gap_scan(None)
        self.scanning = False
        
class Yell:
    def __init__(self):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        
    def advertise(self, name = '!Pico', interval_us=100000):
        short = name[:8]
        payload = struct.pack("BB", len(short) + 1, NAME_FLAG) + name[:8]  # byte length, byte type, value
        self._ble.gap_advertise(interval_us, adv_data=payload)
        
    def stop_advertising(self):
        self._ble.gap_advertise(None)

p = Yell()
c = Sniff(-20)

def yelling(name = '!Fred'):
    p.advertise(name)
    time.sleep(0.01)
    
def sniffing():
    c.scan(0)
    start = time.ticks_ms()
    try:
        while time.ticks_ms() - start < 6*60*1000:
            fred = sum(c.names)
            if fred:
                color[0] = (0,255,0)
                color.write()
            else:
                color[0] = (0,0,255)
                color.write()
            time.sleep(0.001)
    except Exception as e:
        print(e)
    finally:
        c.stop_scan()

yelling('!4')
sniffing()
p.stop_advertising()