from opensplatlibMac import OpenSplatMac
import time

splats = []

def connect(n):
    s = OpenSplatMac(n)
    s.connect()
    splats.append(s)

connect("52050F65-666E-BA3B-C583-685A0BD9A5F4")
# connect(None)

for i in range(14):
    index = 1 << i
    # splats[0]
    first_half = index & 0b11111111
    second_half = index >> 8
    splats[0].setLEDs(first_half, second_half, 255, 0, 0)
    print(f'{i:>2}:{first_half:08b} {second_half:08b}')
    time.sleep(1)

splats[0].allLEDsOff()
