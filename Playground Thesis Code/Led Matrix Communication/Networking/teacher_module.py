from networking import Networking
import time
from machine import Pin, SoftI2C, PWM, ADC
import ledmatrix
import ssd1306
import sensors
import oledicons as pics

sens=sensors.SENSORS()
s = Pin(2, Pin.OUT)

def vibrate(delay=0.2):
    s.value(1)
    time.sleep(delay)
    s.value(0)
    
# Initiate display
i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
a = ledmatrix.LEDMATRIX(i2c)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()
print("Initialising!")

available_messages = [ '5 minutes!', 'Come Inside!']

#Initialise network
networking = Networking(True, False) #First bool is for network info messages, second for network debug messages
broadcast_mac = b'\xff\xff\xff\xff\xff\xff'
networking.aen.add_peer(broadcast_mac, "All")
networking.name = "Teacher"#Set your own device name (this will overwrite the default name gotten from the config.py)

#Variables
hindex = 0
last_press_time = time.ticks_ms()
display_list = []
keyname_dict = {}
name_list = []
searching = True
selected_peer = None

def show_list():
    oled.fill_rect(0, 20, 128, 1, 1)
    oled.fill_rect(0, 21, 128, 44, 0)
    pos = 23
    max_displayed_items = 4
    
    global available_messages, display_list
    display_list = available_messages
    
    if hindex >= 4:
        oled.text("^", 0, 23, 1)
    if hindex/4+1 < len(display_list)//4:
        rotated_caret = [0b00000000,
                         0b00011000,
                         0b00111100,
                         0b01100110,
                         0b00000000,
                         ]
        for row in range(len(rotated_caret)):
            for col in range(8):
                if rotated_caret[row] & (1 << col):
                    oled.pixel(0 + col, 57 + (3 - row), 1)
        #oled.text("v", 0, 53, 1)  # Arrow for items below
        
    start_index = max(0, (hindex//4)*4)    
    for index in range(start_index, min(len(display_list), start_index+4)):
        if index == hindex:
            oled.fill_rect(8, pos-1, 128, 9, 1)  # Highlight selected item
            oled.text(str(display_list[index]), 8, pos, 0)  # Display selected item
        else:
            oled.text(str(display_list[index]), 8, pos, 1)  # Display unselected item
        pos += 10  # Move position down for the next item
    oled.show()
    
def is_cooldown(cooldown):
    global last_press_time
    print(f"Cooldown: {time.ticks_ms()-last_press_time}")
    return (time.ticks_ms() - last_press_time) < cooldown #prevent the scan function from being spammed

def up(pin):
    if is_cooldown(100):
        return
    global last_press_time, hindex, display_list
    last_press_time = time.ticks_ms()
    hindex = (hindex - 1) % len(display_list)  # Wrap around
    show_list()

def down(pin):
    global searching
    searching = True
    if is_cooldown(100):
        return
    global last_press_time, hindex, display_list
    last_press_time = time.ticks_ms()
    print(display_list)
    hindex = (hindex + 1) % len(display_list)  # Wrap around
    show_list()


#Send function
def send(pin):
    global last_press_time
    if(time.ticks_ms()-last_press_time>500):
        last_press_time = time.ticks_ms()
        global available_messages, hindex
        message = available_messages[hindex]
        global broadcast_mac
        networking.aen.send(broadcast_mac, message)
        
#Buttons
switch_down = Pin(8, Pin.IN, Pin.PULL_UP)
switch_select = Pin(9, Pin.IN, Pin.PULL_UP)
switch_up= Pin(10, Pin.IN, Pin.PULL_UP)
# Set up interrupt handlers for button presses
switch_up.irq(trigger=Pin.IRQ_FALLING, handler=down)
switch_down.irq(trigger=Pin.IRQ_FALLING, handler=up)
switch_select.irq(trigger=Pin.IRQ_FALLING, handler=send)

while True:
    show_list()
    time.sleep(1)
