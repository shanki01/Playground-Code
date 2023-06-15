import bluetooth
import time
import ble_CBR

class central:
    def __init__(self):
        ble = bluetooth.BLE()
        ble_CBR.BLESimpleCentral._reset
        self.hub = ble_CBR.BLESimpleCentral(ble)
    
        not_found = False
    
        def on_scan(addr_type, addr, name):
            if addr_type is not None:
                print("Found peripheral:", addr_type, addr, name)
                self.hub.connect()
            else:
                nonlocal not_found
                not_found = True
                print("No peripheral found.")

        self.hub.scan(callback=on_scan)
    
        while not self.hub.is_connected():
            time.sleep_ms(100)
            if not_found:
                return
        print("Connected")
        
        def on_rx(v):
            print("RX", str(bytes(v)))
        
        self.hub.on_notify(on_rx)
    
    def send(self,message):
        try:
            v = message + "_"
            print("TX", v)
            self.hub.write(v)
        except:
            print("TX failed")
        time.sleep_ms(2000)
    
    def respond(self, message): 
        def on_rx(v):
            if self.hub.is_connected():
                # Short burst of queued notifications.
                data = message + "_"
                print("TX", data)
                self.hub.write(data)
        self.hub.on_notify(on_rx)
    def parse_message(v):
        parse = v.decode('ASCII')
        message = parse.replace('_', '')
        return message
    