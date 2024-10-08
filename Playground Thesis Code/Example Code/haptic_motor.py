from machine import Pin, PWM
import time

# Define the pin connected to the motor
motor_pin = Pin(2, Pin.OUT)  # Use the correct GPIO pin for your board

# Set up PWM to control the motor speed
pwm = PWM(motor_pin)

# Set frequency (500-1000Hz is a good starting point for motors)
pwm.freq(1000)

# Function to control motor speed
def motor_speed(duty_cycle):
    pwm.duty_u16(duty_cycle)  # Duty cycle: 0 (off) to 65535 (full speed)

# Turn the motor on at full speed
motor_speed(65535)  # Full speed
time.sleep(2)

# Reduce speed
#motor_speed(32768)  # Half speed
#time.sleep(2)

# Stop the motor
motor_speed(0)  # Motor off
pwm.deinit()  # Turn off PWM