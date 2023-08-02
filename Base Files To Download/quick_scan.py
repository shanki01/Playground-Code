import bluetooth
import time

from ble_advertising import decode_services, decode_name

_IRQ_SCAN_RESULT = 5
_IRQ_SCAN_DONE = 6

class QuickScan:   
    def __init__(self, target): 
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        self.scanning = False
        self.target = target
        self.peripheral = None

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            self.read_scan(data)

        elif event == _IRQ_SCAN_DONE:
            if self.scanning:
                self.scanning = False
                self._ble.gap_scan(None)
        else:
            print('fred')
            print(event)
    def read_scan(self, data):
        addr_type, addr, adv_type, rssi, adv_data = data
        name = decode_name(adv_data)
        addr = bytes(addr)
        if name:
            if self.target in name:
                self.peripheral = name
                print("name: %s"%(name))
                #self.stop_scan()
            
    def scan(self, duration = 2000):
        self.scanning = True
        return self._ble.gap_scan(duration, 30000, 30000)

    def wait_for_scan(self):
        while self.scanning:
            #print('.',end='')
            time.sleep(0.1)
        
    def stop_scan(self):
        self.scanning = False
        self._ble.gap_scan(None)
