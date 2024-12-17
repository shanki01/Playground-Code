#Imports
import time
import struct
from networking import Networking
from led_sequence import LEDSequencer
import ledmatrix
import ssd1306
import sensors
from module import Module
from machine import Pin, SoftI2C, PWM, ADC

module = Module()
num = None
last_num = None
checked = False

def receive():
    global num, checked
    for mac, message, rtime in module.networking.aen.return_messages():
        module.received_message = message
        
        if message == 'coder':
            switch_select.irq(trigger=Pin.IRQ_FALLING, handler=None)
            module.board_mac = mac
            module.screen_display('Accept Coder?')
            start_time = time.time()
            while time.time() - start_time < 5:  # Keep active for 3 seconds
                if switch_select.value() == 0:
                    module.status = 'coder'
                    module.send(module.board_mac, 'coder')
                    time.sleep(0.5)
                    switch_select.irq(trigger=Pin.IRQ_FALLING, handler=select)
                    module.clear_display()
                    module.sequence = []
                    num = None
                    last_num = None
                    break
                time.sleep(0.05)
            module.screen_display(None)
            
        elif message == 'player':
            switch_select.irq(trigger=Pin.IRQ_FALLING, handler=None)
            module.board_mac = mac
            module.screen_display('Accept Player?')
            start_time = time.time()
            while time.time() - start_time < 5:  # Keep active for 3 seconds
                if switch_select.value() == 0:
                    module.status = 'player'
                    module.send(module.board_mac, 'player')
                    time.sleep(0.5)
                    module.clear_display()
                    module.player_sequence = []
                    num = None
                    break
                time.sleep(0.05)
            module.screen_display(None)
            
        elif isinstance(message, list):  #Received a sequence
            module.display_sequence(message)
            
        else: #received a number
            num = int(message)
            checked = False
            
def select(pin):
    global num, last_num
    if module.status == 'coder':
        module.networking.aen.ping(module.board_mac)
        rssi = module.networking.aen.rssi()[module.board_mac][0]
        print(rssi)
        if rssi > -25:
            module.send(module.board_mac, module.sequence)
        #if within trash range:
            #module.reset()
            #num = None
            #last_num = None
        #else:
            #display move closer icon
            
#Callbacks
switch_select = Pin(9, Pin.IN, Pin.PULL_UP)
module.networking.aen.irq(receive)

while True:
    if module.status == 'coder' and module.count < 8:
        if num != last_num and num != None:
            module.add_to_sequence(num)
            module.count += 1
            last_num = num
    elif module.status == 'player' and len(module.sequence) > 0:
        if not checked and num != None:
            matches = module.check_buffer(num)
            checked = True
            if matches:
                module.send(module.board_mac, module.player_sequence)

    time.sleep(2)
                
            
            
            
            
