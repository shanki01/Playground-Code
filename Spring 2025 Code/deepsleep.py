import time
from machine import Pin, deepsleep # type: ignore 
import esp32 # type: ignore 

led = Pin(0, Pin.OUT)
wake_up_button = Pin(2, Pin.IN, Pin.PULL_UP)

# esp32.WAKEUP_ANY_HIGH or esp32.WAKEUP_ALL_LOW
esp32.wake_on_ext1(pins = (wake_up_button,), level = esp32.WAKEUP_ALL_LOW)

def blink_led(times, delay_time):
    for _ in range(times):
        led.value(1)
        time.sleep(delay_time)
        led.value(0)
        time.sleep(delay_time)

blink_led(3, 0.4)

while wake_up_button.value(): 
    print('waiting for button press, and then will go to sleep until button is released')
    time.sleep(1)

deepsleep()
