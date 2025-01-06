import time
import struct
from networking import Networking
from machine import Pin, SoftI2C, PWM, ADC

class Splat:
    def __init__(self, name = '1'): #change to module animal
        self.name = name
        
        #Color dictionary
        self.c = {
        1:'red',
        2:'orange',
        3:'yellow',
        4:'green',
        5:'cyan',
        6:'blue',
        7:'purple',
        8:'pink',
        }
        
        #Note dictionary
        self.n = {
        1:,
        2:,
        3:,
        4:,
        5:,
        6:,
        7:,
        8:,
        }
        
        #Initialize ESPNOW
        self.networking = Networking(True, False) #First bool is for network info messages, second for network debug messages
        self.broadcast_mac = b'\xff\xff\xff\xff\xff\xff'
        self.networking.aen.add_peer(self.broadcast_mac, "All")
        self.networking.name = name
        
        self.modules = ['Lion', 'Tiger', 'Elephant', 'Giraffe', 'Duck', 'Frog', 'Dog', 'Leopard']
        
    def send_to_close_modules(self):
        rssi_buffer = []
        key_buffer = []
        self.networking.aen.ping(self.broadcast_mac)
        time.sleep(0.1)
        for key in networking.aen.rssi():
            rssi = networking.aen.rssi()[key][0]
            if #name of key in self.modules and rssi > cutoff:
                self.networking.aen.send(key, self.name)
    
    def light_on(self):
        color = self.c[int(self.name)]
        #light up splat with color
        
    def play_sound(self):
        note = self.n[int(self.name)]
        #play note on splat
        
