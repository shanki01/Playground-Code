import sensors
import time

#sens = sensor.SENSOR()

#while True:
  #  print(sens.readaccel()[0])
   # time.sleep(1)

from machine import SoftI2C, Pin
from time import sleep
import accel_tap

# Initialize I2C interface
i2c = SoftI2C(scl=Pin(7), sda=Pin(6))

# Initialize the ADXL345 accelerometer
sensor = accel_tap.ADXL345(i2c)


# Enable single-tap detection
sensor.set_tap_threshold(50)  # Adjust the threshold (sensitivity)
sensor.set_tap_duration(15)   # Adjust tap duration for better responsiveness

# Enable the tap detection interrupt on axis
sensor.enable_tap_detection(single_tap=True, double_tap=False)

while True:
    if sensor.is_tapped():
        print("Tap detected!")
    
    sleep(0.1)
