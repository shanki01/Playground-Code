import bluetooth
import ble_SMH
import time

class peripheral:
    
    flag = False
    
    def __init__(self, name = 'Spike'):    
        ble = bluetooth.BLE()
        
        self.hub = ble_CBR_short.BLESimplePeripheral(ble, 'UART', name)
        print(name)
    
    def advertise(self):
        self.hub._advertise()
