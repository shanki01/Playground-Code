
import max7219
from machine import Pin, SPI
import framebuf
import time

import machine, neopixel
import time

NUM_LEDS = 100
np = neopixel.NeoPixel(machine.Pin(21), NUM_LEDS)

np.fill((0,0,0)) # set to neopixels off, full brightness
np.write()

def hue(pos, brightness=10):
    """
    Generate RGB color across 0-255 positions.
    
    :param pos: Position in the color wheel (0-255)
    :return: Tuple (R, G, B) - the color corresponding to the position
    """
    bright_scale = brightness/10
    
    if pos < 85:
        return (int((255 - pos*3)*bright_scale), int((pos * 3)*bright_scale), 0)  # 0 is red
    elif pos < 170:
        pos -= 85
        return (0, int((255 - pos*3)*bright_scale), int((pos * 3)*bright_scale))  # 85 is green
    else:
        pos -= 170
        return (int((pos*3)*bright_scale), 0, int((255 - pos * 3)*bright_scale))  # 170 is blue


def rainbow_cycle(wait, count, brightness=10):
    """Display a rainbow cycle across the entire LED strip."""
    for j in range(256):  # Loop through 256 color positions
        print(j)
        for i in range(count):  # Loop through each LED
            pixel_index = (i * 256 // count) + j  # Calculate color position
            np[i] = hue(pixel_index & 255, brightness)  # Set the LED to the color
        np.write() 
        time.sleep(wait)  # Pause for a short time before the next update
        

# Initialize MAX7219 display (8x32)
spi = SPI(1, baudrate=10000000, sck=Pin(8), mosi=Pin(10))
display = max7219.Max7219(64, 8, spi, Pin(2))
display.brightness(2)
 
display.draw_5x3_string(" HELLO! ")
display.show()
        
rainbow_cycle(.001, 9, 1)
rainbow_cycle(.001, 9, 1)
rainbow_cycle(.001, 9, 1)
rainbow_cycle(.001, 9, 1)
np.fill((0,0,0)) # set to neopixels off, full brightness
np.write()

