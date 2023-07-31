import bluetooth
import random
import struct
import time

from ble_advertising import decode_services, decode_name

_IRQ_SCAN_RESULT = 5
_IRQ_SCAN_DONE = 6

_ADV_IND = 0x00
_ADV_DIRECT_IND = 0x01
_ADV_SCAN_IND = 0x02

class ScanCentral:   
    def __init__(self, ble): 
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self.peripheral = None
        
        self._reset()

    def _reset(self):
        # Cached name and address from a successful scan.
        self._name = None
        self._addr_type = None
        self._addr = None
        self.addresses = set()
        self._read_callback = None
        self._done_callback = None
        self.scanning = False

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            if self._read_callback(data):
                self.scanning = False
                self._ble.gap_scan(None)
                self._reset()

        elif event == _IRQ_SCAN_DONE:
            self.scanning = False
            if self._done_callback:
                if self._addr:
                    # Found a device during the scan (and the scan was explicitly stopped).
                    self._done_callback(self._addr_type, self._addr, self._name)
                    self._done_callback = None
                else:
                    # Scan timed out.
                    self._done_callback(None, None, None)

    # Find a device advertising the environmental sensor service.
    def scan(self, read_cb = None, done_cb = None, duration = 2000):
        self._reset()
        self._read_callback = read_cb
        self._done_callback = done_cb
        self.scanning = True
        #run for 2 sec, with checking every 30 ms for 30 ms
        return self._ble.gap_scan(duration, 30000, 30000)

    def wait_for_scan(self):
        while self.scanning:
            time.sleep(0.5)

    def stop_scan(self):
        print('stopping scan')
        self._ble.gap_scan(None)
