import time
from rssi_ble import Sniff, Yell

def central():
    c = Sniff(cutoff=-60)
    c.scan(0)   # 0ms = scans forever
    while True:
        latest = c.name
        if latest:
            c.last='' # clear the flag for the next advertisement
            print(f'Got: {latest}')
        time.sleep(0.5)

def peripheral():
    p = Yell()
    while True:
        p.advertise(f'!Pico')
        time.sleep(0.1)
    # p.stop_advertising()

central()
# peripheral()
