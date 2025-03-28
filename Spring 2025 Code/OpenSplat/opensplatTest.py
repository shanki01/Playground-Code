from opensplatlib import OpenSplat
from time import sleep
from datetime import datetime
import random

splats = []

def connect(n):
    s = OpenSplat(n)
    s.connect()
    splats.append(s)
    print("Connected to Splat #" + str(len(splats)))

#connect("ab:42:00:00:20:06")
#connect("ab:42:00:00:20:39")
connect("ab:42:00:00:20:e7")
connect("ab:42:00:00:24:75")

for i in range(0, 80):
    #for j in range(0, len(splats)):
        #splats[j].playSound(1, 255)   # sample 8, max volume
        #splats[j].setLEDs(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #splats[j].setLEDs(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #splats[j].setLEDs(255, 0, 255, 0, 0)
        #splats[j].setLEDs(0, 255, 0,  255, 0)
        #splats[j].setLEDs(255, 0, 255, 255, 0)
        #splats[j].setLEDs(0, 255, 0, 0, 255)
   #print(datetime.now().microsecond)
   splats[0].playSound(i, 255)
   #print(datetime.now().microsecond)
   splats[1].playSound(i+1, 255)
        #splats[j].allLEDsOff()
   sleep(.25)

