#Code for hub acting as central with a sensor sending info to peripheral actuator hub
import bluetooth
import numpy as np
import time
import ble_CBR
from central_functions import central
import hub as spike
import color_sensor, color

light_matrix.clear()

pixels_tl = [[1,1],[1,2],[2,1],[2,2]]
pixels_tr = [[5,1],[5,2],[4,1],[4,2]]
pixels_bl = [[1,5],[1,4],[2,5],[2,4]]
pixels_br = [[4,4],[4,5],[5,4],[5,5]]

pixels = [pixels_tl,pixels_bl,pixels_tr,pixels_br]

while True:
    device = central()
    count = 0
    try:
        connected = device.is_connected()
        if connected:
            while connected:
                connected = device.is_connected()
                color_tl = color_sensor.color(spike.port.A)
                color_bl = color_sensor.color(spike.port.C)
                color_tr = color_sensor.color(spike.port.B)
                color_br = color_sensor.color(spike.port.D)
                colors = list(map(abs,[color_tl,color_bl,color_tr,color_br]))
                for i in range(4):
                    if colors[i] == 0:
                        for j in range(4):
                            spike.light_matrix.set_pixel(pixels[i][j][0]-1,pixels[i][j][1]-1,100)
                    else:
                        for j in range(4):
                            spike.light_matrix.set_pixel(pixels[i][j][0]-1,pixels[i][j][1]-1,0)
                if spike.button.pressed(2) > 0:
                    device.send(str(colors))
                    time.sleep(0.5)
                time.sleep(0.1)
    except:
        time.sleep(2)

