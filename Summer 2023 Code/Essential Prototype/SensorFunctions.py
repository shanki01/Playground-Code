import hub

import time
#------------------------------------------------------------------------------------
def get_distance(port):
    while True:
        dis = hub.status()['port'][port]
        if len(dis) > 0:
            if dis[0] != None:
                dis = dis[0]
                break
    return dis
#------------------------------------------------------------------------------------
def get_tilt():
    while True:
        acc = hub.status()['yaw_pitch_roll']
        if acc != [0,0,0]:
            return acc
#------------------------------------------------------------------------------------
def reset_tilt():
    a = get_tilt()
    offset = [a[0]*-1, a[1]*-1, a[2]*-1]
    return offset
#------------------------------------------------------------------------------------
def update_range(value, old_min, old_max, new_min, new_max):
    new_value = (value-old_min)*(new_max-new_min)/(old_max-old_min) + new_min
    return new_value
#------------------------------------------------------------------------------------
def bound_value(value, low, high):
    if value > high:
        value = high
    elif value < low:
        value = low
    return value
#------------------------------------------------------------------------------------

#for i in range(10):
#    print(get_distance())
#    time.sleep(0.2)

#print("something")
"""
motor = hub.port.B.motor
if motor != None:
    motor.preset(0)


off = reset_tilt()

for i in range(100):
    tilt_a = get_tilt()
    tilt_b = [0,0,0]
    for i in range(3):
        tilt_b[i] = tilt_a[i] + off[i]
    
    new_speed = 10*round(update_range(tilt_b[1], -45, 45, -100, 100)/10)
    if new_speed > 100:
        new_speed = 100
    if new_speed < -100:
        new_speed = -100
    
    new_tilt = tilt_b[2]
    if new_tilt > 45:
        new_tilt = 45
    elif new_tilt < -45:
        new_tile = -45
    
    #If in the middle, light up a certain color
    
    motor_command = [new_speed, new_tilt]
    print(motor_command)
    
    time.sleep(0.1)

    """
    
"""

Tilt forward - move forward at speed relative to tilt angle
Tilt left - turn left at angle relative to tilt angle
Tilt right  - turn right at angle relative to tilt angle
Tilt back - Move backward at speed relative to tilt angle

Command format - [speed forward or backward, tilt]
[a, b, c] - [speed, turn_angle]



"""
#for i in range(100):
#    a = get_distance('A')
#    print(i, a)
#    time.sleep(0.1)