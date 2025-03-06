from machine import Pin,lightsleep,SLEEP
from time import sleep_ms
import machine
import time

led = Pin(3, Pin.OUT)

def blink_led(times, delay_time):
    for _ in range(times):
        led.value(1)
        time.sleep(delay_time)
        led.value(0)
        time.sleep(delay_time)
blink_led(3, 0.4)
import esp32


wake_up = Pin(2, Pin.IN, Pin.PULL_UP)

#sp32.WAKEUP_ANY_HIGH or esp32.WAKEUP_ALL_LOW
esp32.wake_on_ext1(pins = (wake_up,), level = esp32.WAKEUP_ALL_LOW)


print('Im awake now. Going to sleep in 5 seconds ...')
#time.sleep(5)
print('Going to sleep now ..')

machine.deepsleep()
