import ble_SMH

class central:
      
    def __init__(self, target = 'Spike'):
        ble_SMH.BLESimpleCentral._reset
        self.hub = ble_SMH.BLESimpleCentral(target)
        self.per_name = None
        
    def scan(self, duration):         
        self.hub.scan(duration)
        self.hub.wait_for_scan()
        self.per_name = self.hub.peripheral
     
    def connect(self):
        self.scan(0)
        self.hub.wait_for_scan()
        self.hub.connect()
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
        
    def on_notify(self, callback):
        self.hub.on_notify(callback)
        
    def disconnect(self):
        self.hub.disconnect()
        
    def is_connected(self):
        return self.hub.is_connected()
        
        
        
class peripheral:
    
    def __init__(self, name = 'Spike'):    
        ble = bluetooth.BLE()
        
        self.hub = ble_SMH.BLESimplePeripheral(ble, 'UART', name)
        
        def on_rx(v):
            print("RX", str(bytes(v)))
        
        self.hub.on_write(on_rx)
    
    def advertise(self):
        self.hub._advertise()
        
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
        
    def on_notify(self, callback):
        self.hub.on_write(callback)
        
    def disconnect(self):
        self.hub.disconnect()
        
    def is_connected(self):
        return self.hub.is_connected()

