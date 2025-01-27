import time
import struct
from networking import Networking
from led_sequence import LEDSequencer
import ledmatrix
import ssd1306
import sensors
import icons
from machine import Pin, SoftI2C, PWM, ADC

#Define module class
class Module:
    def __init__(self, name = 'Lion'): #change to module animal
        self.status = 'Searching'
        self.last_status = None
        self.board_mac = None
        self.board_rssi = None
        self.count = 0
        self.sequence = []
        self.player_sequence = []
        self.screen_message = None
        self.received_message = None
        self.last_message = None
        self.complete = False
        self.motor = Pin(2, Pin.OUT)
        self.sens = sensors.SENSORS()
        
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
        
        #Initialize ESPNOW
        self.networking = Networking(True, False) #First bool is for network info messages, second for network debug messages
        self.broadcast_mac = b'\xff\xff\xff\xff\xff\xff'
        self.networking.aen.add_peer(self.broadcast_mac, "All")
        self.networking.aen.ping(self.broadcast_mac)
        self.networking.name = name
        
        #oled screen
        self.i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
        self.oled = icons.SSD1306_SMART(128, 64, self.i2c)
        self.clear_oled()

        #Led Matrix setup
        self.matrix = ledmatrix.LEDMATRIX(self.i2c)
        self.sequencer = LEDSequencer(self.matrix)
        self.buffer = self.sequencer.buffer
        self.clear_display()
        
    def clear_display(self):
        self.sequencer.clear_display()
        
    def clear_oled(self):
        self.oled.fill(0)
        self.oled.show()
        
    def displaybatt(self, p):
        batterycharge=self.sens.readbattery()
        self.oled.showbattery(batterycharge)
        return batterycharge
    
    def checkstatus(self,p):
        if self.screen_message == None and self.status != self.last_status:
            self.screen_display(self.status)
        if self.board_mac != None:
            self.networking.aen.ping(self.board_mac)
            self.board_rssi = self.networking.aen.rssi()[self.board_mac][0]
            
    def board_name(self):
        return self.networking.aen.peer_name(self.board_mac)
        
    def vibrate(self, delay = 0.2):
        self.motor.value(1)
        time.sleep(delay)
        self.motor.value(0)
    
    def send(self, mac, message):
        self.networking.aen.send(mac, message)
    
    def screen_display(self, message):
        self.screen_message = message
        if message == None:
            self.oled.fill_rect(0,20,128,40,0)
        else:
            self.oled.text(message,0,20,1)
        self.oled.show()
    
    def display_sequence(self,sequence):
        self.sequence = sequence
        for i in range(0,len(sequence)):
            num = sequence[i]
            color = self.c[num]
            self.sequencer.display_color_pixel(color,7-i,7)
        self.sequencer.display_number(sequence[0],self.c[sequence[0]])
        
    def display_player_sequence(self):
        for i in range(0,len(self.player_sequence)):
            num = self.player_sequence[i]
            color = self.c[num]
            self.sequencer.display_color_pixel(color,7-i,6)
    
    def display_wrong(self):
        for i in range(0,8):
            self.sequencer.display_color_pixel('red',7-i,6)
        time.sleep(0.75)
        for i in range(0,8):
            self.sequencer.display_color_pixel('black',7-i,6)
    
    def display_correct(self):
        buffer = [0x52]*64
        self.matrix.display_frames(buffer, 1000,1,1)
        self.complete = True
        
    def add_to_sequence(self,num):
        self.sequence.append(num)
        color = self.c[num]
        self.sequencer.display_number(num,color)
        self.sequencer.display_color_pixel(color,7-(len(self.sequence)-1),7)
    
    def check_buffer(self,num):
        index = len(self.player_sequence)
        color = self.c[num]
        print(7-(len(self.player_sequence)-1))
        self.sequencer.display_color_pixel(color,7-index,6)
        if num == self.sequence[index]:
            self.player_sequence.append(num)
            if (index + 1) < len(self.sequence):
                self.sequencer.display_number(self.sequence[index+1],self.c[self.sequence[index+1]])
            else:
                self.display_correct()
            return True
        else:
            self.vibrate()
            self.display_wrong()
            self.display_player_sequence()
            return False
    
    def switch_status(self, status, mac):
        self.board_mac = mac
        self.screen_display(None)
        self.clear_display()
        self.sequence = []
        if status == 'Coder':
            self.status = status
            self.count = 0
        elif 'Player' in status:
            self.status = 'Player'
            self.player_sequence = []
        self.send(self.board_mac, status)