#Imports
import time
import struct
from networking import Networking
from led_sequence import LEDSequencer
import ledmatrix
import ssd1306
import sensors
from module import Module
from machine import Pin, SoftI2C, PWM, ADC, Timer

module = Module('Elephant')
num = None
last_num = None
checked = False
in_range = False

def receive():
    global num, last_num, checked
    for mac, message, rtime in module.networking.aen.return_messages():
        module.received_message = message
        
        if message == 'Coder':
            switch_select.irq(trigger=Pin.IRQ_FALLING, handler=None)
            module.board_mac = mac
            module.screen_display(None)
            module.screen_display('Accept Coder?')
            start_time = time.time()
            while time.time() - start_time < 5:  # Keep active for 3 seconds
                if switch_select.value() == 0:
                    module.screen_display(None)
                    module.status = 'Coder'
                    print('Coder Accepted')
                    module.send(module.board_mac, 'Coder')
                    module.sequence = []
                    num = None
                    last_num = None
                    module.count = 0
                    break
                time.sleep(0.05)
            module.screen_display(None)
            if module.status == 'Coder':
                switch_select.irq(trigger=Pin.IRQ_FALLING, handler=select)
            
        elif message == 'Player':
            switch_select.irq(trigger=Pin.IRQ_FALLING, handler=None)
            module.board_mac = mac
            module.screen_display(None)
            module.screen_display('Accept Player?')
            start_time = time.time()
            while time.time() - start_time < 5:  # Keep active for 5 seconds
                if switch_select.value() == 0:
                    module.screen_display(None)
                    module.status = 'Player'
                    print('Player Accepted')
                    module.send(module.board_mac, 'Player')
                    time.sleep(0.5)
                    module.player_sequence = []
                    num = None
                    break
                time.sleep(0.05)
            module.screen_display(None)
            if module.status == 'Coder':
                switch_select.irq(trigger=Pin.IRQ_FALLING, handler=select)
            
        elif isinstance(message, list):  #Received a sequence
            module.display_sequence(message)
            
        else:   #received a number
            if module.board_name() == 'Music' and module.status == 'Coder':
                module.screen_display(None)
                module.screen_display('Add Note?')
                switch_select.irq(trigger=Pin.IRQ_FALLING, handler=None)
                start_time = time.time()
                while time.time() - start_time < 3:  # Keep active for 3 seconds
                    if switch_select.value() == 0:
                        module.screen_display(None)
                        module.vibrate()
                        print('Note Added')
                        num = int(message)
                        checked = False
                        break
                module.screen_display(None)
                if module.status == 'Coder':
                    switch_select.irq(trigger=Pin.IRQ_FALLING, handler=select)
            else:
                num = int(message)
                checked = False
            
def select(pin):
    global num, last_num, sent
    if module.status == 'Coder':
        if module.board_rssi > -40:
            module.send(module.board_mac, module.sequence)
            module.screen_display(None)
            module.screen_display('Sent')
            time.sleep(2)
            module.screen_display(None)
        #if within trash range:
            #module.reset()
            #num = None
            #last_num = None
        #else:
            #display move closer icon
            
#Callbacks
switch_select = Pin(9, Pin.IN, Pin.PULL_UP)
module.networking.aen.irq(receive)
batt = Timer(2)
batt.init(period=1000, mode=Timer.PERIODIC, callback=module.displaybatt)
status = Timer(0)
status.init(period=3000, mode=Timer.PERIODIC, callback=module.checkstatus)

while True:
    if module.status == 'Coder':
        if module.count < 8:
            if num != None:
                if module.board_name() == 'Music' or num != last_num:
                    module.add_to_sequence(num)
                    module.count += 1
                    last_num = num
        if module.count > 0:
            while module.board_rssi > -40:
                if module.screen_message != 'Send?':
                    in_range = True
                    module.screen_display(None)
                    module.screen_display('Send?')
            if in_range:
                module.screen_display(None)
                in_range = False
            
    elif module.status == 'Player' and len(module.sequence) > 0:
        if not checked and num != None:
            matches = module.check_buffer(num)
            checked = True
            if matches:
                module.send(module.board_mac, module.player_sequence)

    time.sleep(2)
