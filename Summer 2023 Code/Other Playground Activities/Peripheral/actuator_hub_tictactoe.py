#Code for hub acting as peripheral with an actuator responding to a sensor on the central hub
import bluetooth
import time
import ble_CBR
from peripheral_functions import peripheral
import hub as spike
import motor

light_matrix.clear()

pixels_tl = [[1,1],[1,2],[2,1],[2,2]]
pixels_tr = [[5,1],[5,2],[4,1],[4,2]]
pixels_bl = [[1,5],[1,4],[2,5],[2,4]]
pixels_br = [[4,4],[4,5],[5,4],[5,5]]

pixels = [pixels_tl,pixels_bl,pixels_tr,pixels_br]

device = peripheral()

def on_rx(v):
    parse = v.decode('ASCII')
    message = list(parse.replace('_', ''))
    print(message)
    colors = []
    for i in range(4):
        colors.append(message[(3*i)+1])
    print("RX",colors)
    for i in range(4):
        if colors[i] == '0':
            for j in range(4):
                spike.light_matrix.set_pixel(pixels[i][j][0]-1,pixels[i][j][1]-1,100)
        else:
            for j in range(4):
                spike.light_matrix.set_pixel(pixels[i][j][0]-1,pixels[i][j][1]-1,0)

device.on_notify(on_rx)

while True:
    connected = device.is_connected()
    if connected:
        time.sleep(2)           
    else:
        time.sleep(2)
        device.on_notify(on_rx)
        time.sleep(2)
