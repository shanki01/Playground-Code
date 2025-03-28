from opensplatlibMac import OpenSplatMac
from time import sleep

splats = []

def connect(n):
    s = OpenSplatMac(n)
    s.connect()
    splats.append(s)

# connect("52050F65-666E-BA3B-C583-685A0BD9A5F4")
# connect(None)

for i in range(14):
    print()

# splats[0].setLEDs(0b00000001, 0b00000000, 255, 0, 0) # LED 0
# input('Press Enter to continue')
# splats[0].setLEDs(0b00000010, 0b00000000, 255, 0, 0) # LED 1
# splats[0].setLEDs(0b00000100, 0b00000000, 255, 0, 0) # LED 2
# splats[0].setLEDs(0b00001000, 0b00000000, 255, 0, 0) # LED 3
# splats[0].setLEDs(0b00010000, 0b00000000, 255, 0, 0) # LED 4
# splats[0].setLEDs(0b00100000, 0b00000000, 255, 0, 0) # LED 5
# splats[0].setLEDs(0b01000000, 0b00000000, 255, 0, 0) # LED 6
# splats[0].setLEDs(0b10000000, 0b00000000, 255, 0, 0) # LED 7
# splats[0].setLEDs(0b00000000, 0b00000001, 255, 0, 0) # LED 8
# splats[0].setLEDs(0b00000000, 0b00000010, 255, 0, 0) # LED 9
# splats[0].setLEDs(0b00000000, 0b00000100, 255, 0, 0) # LED 10
# splats[0].setLEDs(0b00000000, 0b00001000, 255, 0, 0) # LED 11
# splats[0].setLEDs(0b00000000, 0b00010000, 255, 0, 0) # LED 12
# splats[0].setLEDs(0b00000000, 0b00100000, 255, 0, 0) # LED 13
#
#
# input('Press Enter to continue')
#
# splats[0].setLEDs(0, 255, 0,  255, 0) # set other half of LEDs to GREEN
# input('Press Enter to continue')
#
# splats[0].setLEDs(255, 0, 255, 255, 0) # set x LEDs to YELLOW
# input('Press Enter to continue')
#
# splats[0].setLEDs(0, 255, 0, 0, 255) # set other half of LEDs to BLUE
# input('Press Enter to continue')

splats[0].allLEDsOff()