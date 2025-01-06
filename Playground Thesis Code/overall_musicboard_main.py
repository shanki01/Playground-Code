from machine import Pin, SPI, Timer
import espnow
from networking import Networking
import time
import ujson as json
import os
import time

# --- ESP-NOW Setup ---
networking = Networking(True, False) #First bool is for network info messages, second for network debug messages
broadcast_mac = b'\xff\xff\xff\xff\xff\xff'
networking.aen.add_peer(broadcast_mac, "All")
networking.aen.ping(broadcast_mac)
networking.name = 'Music Board'

sequence = []

# --- Button Setup ---
coder_button = Pin(9, Pin.IN, Pin.PULL_UP)
#ADD PLAY BUTTON
  
#---Broadcast Functions---
def send_to_close_modules(message, cutoff):
    rssi_buffer = []
    key_buffer = []
    networking.aen.ping(broadcast_mac)
    time.sleep(0.1)
    for key in networking.aen.rssi():
        rssi = networking.aen.rssi()[key][0]
        if rssi > cutoff:
            networking.aen.send(key, message)

# --- Button Handlers ---
def add_coder_handler(pin):
    """Handler to initiate adding a coder."""
    print("Requesting coder...")
    send_to_close_modules('coder', -40)

def play_music_handler(pin):
    if len(sequence) > 0:
        #PLAY SEQUENCE AND ANIMATE LIGHTS


# Assign button handlers
coder_button.irq(trigger=Pin.IRQ_FALLING, handler=add_coder_handler)
#ADD PLAY BUTTON HANDLER

# --- ESP-NOW Receive Handler ---
def on_receive_callback():
    for mac, msg, rtime in networking.aen.return_messages():
        # Handle coder confirmation
        if msg == 'coder':
            print(f"Coder confirmed: {mac}")

        # Handle sequence broadcast
        elif isinstance(msg, list):
            global sequence
            sequence = msg
            print(f"Sequence received: {sequence}")
            #LIGHT UP SEQUENCE ON BOARD

networking.aen.irq(on_receive_callback)

# --- Main Loop ---
def main():
    print("Music controller initialized. Waiting for input...")
    while True:
        time.sleep(0.5)

if __name__ == "__main__":
    main()