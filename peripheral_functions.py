import bluetooth
import ble_CBR
import time

class peripheral:
    def __init__(self):    
        ble = bluetooth.BLE()
        
        self.hub = ble_CBR.BLESimplePeripheral(ble, 'UART', 'Spike')
        
        def on_rx(v):
            print("RX", str(bytes(v)))
        
        self.hub.on_write(on_rx)
        
    def respond(self, message): 
        def on_rx(v):
            if self.hub.is_connected():
                # Short burst of queued notifications.
                data = message + "_"
                print("TX", data)
                self.hub.send(data)
        self.hub.on_write(on_rx)
        
    def received(self): 
        def on_rx(v):
            message = str(bytes(v))
            print("got",message)
            return message
        self.hub.on_write(on_rx)
        
    def send(self, message):
        try:
            v = message + "_"
            print("TX", v)
            self.hub.send(v)
        except:
            print("TX failed")
        time.sleep_ms(2000)
        
    def parse_message(self, v):
        parse = v.decode('ASCII')
        message = parse.replace('_', '')
        return message
        