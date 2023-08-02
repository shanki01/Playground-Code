from machine import ADC, Pin

color_button = Pin(4, Pin.IN, Pin.PULL_DOWN)
def on_press(pin):
    print('pressed')
color_button.irq(on_press)