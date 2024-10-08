# Define the crown as a sequence of 64-bit values (same as Arduino format)
crown_frames = [
    0xffff5e5e5e5effff,
    0xff5effffffff5eff,
    0x5eff5effff5eff5e,
    0x5effffffffffff5e,
    0x5eff5effff5eff5e,
    0x5effff5e5effff5e,
    0xff5effffffff5eff,
    0xffff5e5e5e5effff
]

# Create an instance of the LEDMATRIX class
from machine import Pin, SoftI2C

# Initialize I2C
i2c = SoftI2C(scl=Pin(7), sda=Pin(6))

# Import the LED matrix class
import ledmatrix
matrix = ledmatrix.LEDMATRIX(i2c)

# Convert 64-bit integers into byte arrays for each frame
def convert_to_bytes(frame_data):
    byte_list = []
    for frame in frame_data:
        # Convert each 64-bit integer to a sequence of 8 bytes (big-endian)
        byte_list.extend(frame.to_bytes(8, 'big'))
    return byte_list

# Convert crown frames into a 64-byte buffer
frame_buffer = convert_to_bytes(crown_frames)

# Display the frame for 200ms, without repeating forever
matrix.display_frames(frame_buffer, duration_time=200, forever_flag=1, frames_number=1)




