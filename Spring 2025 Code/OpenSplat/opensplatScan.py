from bluepy.btle import Scanner, DefaultDelegate, Peripheral

addr = ""

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
       for (adtype, desc, value) in dev.getScanData():
           if (value == "SPLAT") | (value == "Splat"):
               print("Found SPLAT {}" . format(dev.addr))
               #peripheral = Peripheral(dev.addr, iface=0)
               print("Connected!")

scanner = Scanner().withDelegate(ScanDelegate())
print("Scanning...")
devices = scanner.scan(10.0)

