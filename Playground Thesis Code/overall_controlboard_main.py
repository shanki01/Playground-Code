from machine import Pin, SPI, Timer
import espnow
from networking import Networking
import time
import ujson as json
import os
from playertracker import PlayerTracker
from gamestate import GameState
from max7219 import Max7219
import time

# --- Pin Constants for XIAO ESP32-C3 ---
CODER_BUTTON_PIN = 3          
UNDO_BUTTON_PIN = 20
RANDOM_BUTTON_PIN = 9
PLAYER_BUTTON_PINS = [4, 5, 6, 7]  
NEOPIXEL_PIN = 21       
SPI_SCK_PIN = 8               
SPI_MOSI_PIN = 10             
MAX7219_CS_PIN = 2            

# --- Constants ---
INACTIVITY_TIMEOUT = 600  # 10 minutes in seconds
DISCONNECTION_TIMEOUT = 300  # 5 minutes in seconds
GAME_STATE_FILE = "game_state.json"
REQUEST_TIMEOUT = 5  # 5 seconds for request timeout

# --- ESP-NOW Setup ---
networking = Networking(True, False) #First bool is for network info messages, second for network debug messages
broadcast_mac = b'\xff\xff\xff\xff\xff\xff'
networking.ap._ap.active(False)
networking.aen.add_peer(broadcast_mac, "All")
networking.aen.ping(broadcast_mac)
networking.name = 'Control Board'

# --- Initialize Classes ---
game_state = GameState(coder_mac=None)
player_tracker = PlayerTracker(pin=NEOPIXEL_PIN)

# --- MAX7219 Setup ---
spi = SPI(1, baudrate=10000000, sck=Pin(SPI_SCK_PIN), mosi=Pin(SPI_MOSI_PIN))
cs = Pin(MAX7219_CS_PIN, Pin.OUT)
max_display = Max7219(64, 8, spi, cs)  # 8 matrices (64 pixels wide, 8 pixels high)
max_display.text("READY GO",0,0,1)
max_display.show()


# --- Button Setup ---
coder_button = Pin(CODER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
undo_button = Pin(UNDO_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
random_button = Pin(RANDOM_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
player_buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in PLAYER_BUTTON_PINS]

# --- Save and Load Game State ---
def save_game_state(filename):
    """Save the current game state to a file."""
    with open(filename, "w") as f:
        json.dump(game_state.to_dict(), f)
    print("Game state saved.")

def load_game_state(filename):
    """Load the game state from a file."""
    with open(filename, "r") as f:
        data = json.load(f)
        game_state.from_dict(data)
        player_tracker.reset_all_progress()
        print("Previous game state loaded.")

def backup_and_load_previous_game():
    """Backup the current game and load the previous game state."""
    if os.path.exists(GAME_STATE_FILE):
        save_game_state("backup_" + GAME_STATE_FILE)
        load_game_state(GAME_STATE_FILE)
  
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
def button_detect_long_press(pin, duration=200):
    start = time.ticks_ms()
    while time.ticks_ms()-start<duration:
        time.sleep(duration/10000)
        # print(time.ticks_ms()-start<duration,":",pin.value())
        if pin.value():
           return False
    while not pin.value(): #wait for release
        print("held")
        time.sleep(duration/100000)
    time.sleep(duration/2000)
    return True
    
def add_coder_handler(pin):
    """Handler to initiate adding a coder."""
    print("Requesting coder...")
    if button_detect_long_press(pin):
        max_display.draw_5x3_string("NEW GAME!")
        max_display.show()
        player_tracker.indicate_request(4, color=(0, 0, 255))  # Blue light for coder request
        send_to_close_modules('Coder', -60)
    else:
        print("Code Button Released Early")
        

def add_player_handler(pin, player_number):
    """Handler to initiate adding a specific player."""
    print(f"Requesting player...")
    if button_detect_long_press(pin):
        player_tracker.indicate_request(player_number-1, color=(255, 0, 0))  # Green light for player request
        send_to_close_modules('Player' + str(player_number), -60)
    else:
        print("Player Button Released Early")

def undo_handler(pin):
    """Handler to recover the previous game state."""
    if button_detect_long_press(pin):
        print("Undoing last reset...")
        backup_and_load_previous_game()

def shuffle_handler(pin):
    """Handler to recover the previous game state."""
    if button_detect_long_press(pin):
        print("Undoing last reset...")
        backup_and_load_previous_game()

# Assign button handlers
coder_button.irq(trigger=Pin.IRQ_FALLING, handler=add_coder_handler)
undo_button.irq(trigger=Pin.IRQ_FALLING, handler=undo_handler)

def create_handler(num):
    # Returns a handler function specific to the player number
    def handler(pin):
        add_player_handler(pin, num)
    return handler

for i, button in enumerate(player_buttons):
    button.irq(trigger=Pin.IRQ_FALLING, handler=create_handler(i + 1))


# --- ESP-NOW Receive Handler ---
def on_receive_callback():
    for mac, msg, rtime in networking.aen.return_messages():
        print('received',msg,type(msg))
        # Handle coder confirmation
        if msg == 'Coder':
            game_state.coder_mac = mac
            player_tracker.clear_all()
            print(f"Coder confirmed: {mac}")
            max_display.draw_5x3_string("CODING")
            max_display.show()
            player_tracker.indicate_request(4, (0,0,0))
           

        # Handle player confirmation
        elif 'Player' in msg:
            game_state.add_player(mac)
            if len(game_state.sequence) > 0:
                networking.aen.send(mac, game_state.sequence) #if coder sequence is already "dumped", player "picks it up"
            player_index = msg[-1]
            player_tracker.indicate_request(player_index-1, (0,0,0))
            print(f"Player confirmed: {mac}")

        # Handle sequence broadcast
        elif isinstance(msg, list):
            # Handle coder sequence
            if mac == game_state.coder_mac:
                sequence = msg
                if len(game_state.sequence) == 0:   #if no coder sequence before and players registered, send to registered players
                    print(game_state.players)
                    for key in game_state.players:
                        networking.aen.send(key, sequence)
                save_game_state(GAME_STATE_FILE)
                print('saving game state')
                player_tracker.reset_all_progress()
                game_state.set_sequence(sequence)
                player_tracker.display_coder_sequence(sequence)
                max_display.draw_5x3_list(sequence)
                max_display.show()
                    
                print(f"Sequence received: {sequence}")
            # Handle player progress update    
            else:
                step = len(msg)
                if mac in game_state.players:
                    game_state.update_progress(mac, step)
                    player_index = list(game_state.players.keys()).index(mac)
                    player_tracker.update_player_progress(player_index, step, game_state.sequence)
                    print(f"Player {player_index} updated to step {step}")

networking.aen.irq(on_receive_callback)

# --- Main Loop ---
def main():
    print("Game controller initialized. Waiting for input...")
    while True:
        time.sleep(0.5)

if __name__ == "__main__":
    main()