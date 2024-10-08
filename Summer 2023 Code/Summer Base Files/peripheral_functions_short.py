import bluetooth
import ble_SMH
import time

class peripheral:
    
    flag = False
    
    def __init__(self, name = 'Spike'):    
        ble = bluetooth.BLE()
        
        self.hub = ble_SMH.BLESimplePeripheral(ble, 'UART', name)
    
    def advertise(self, name):
        self.hub._advertise(name)