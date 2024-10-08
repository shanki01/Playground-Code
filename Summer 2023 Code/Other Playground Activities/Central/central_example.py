# This is from Damien's example - running the UART Central

import bluetooth
import time
import ble_CBR
from central_functions import central

def demo():
    
    device = central()
    
    def on_rx(v):
        print("RX", str(bytes(v)))

    device.on_notify(on_rx)

    with_response = False

    while device.is_connected():
        try:
            v = 'hello' + "_"
            print("TX", v)
            device.send(v)
        except:
            print("TX failed")
        time.sleep_ms(4000)
    device.disconnect()
    print("Disconnected")

demo()
