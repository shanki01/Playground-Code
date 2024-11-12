class LEDSequencer:
    def __init__(self, matrix):
        self.matrix = matrix
        self.buffer = [0xff] * 64  # Initialize with all pixels off (black)

    def display_color_at_location(self, color, x, y):
        # Update the buffer at the specified (x, y) position
        index = y * 8 + x
        self.buffer[index] = color

        # Display the updated buffer
        duration_time = 1000  # Duration for the display, in milliseconds
        forever_flag = 1      # Display continuously until interrupted
        frames_number = 1     # Single frame

        self.matrix.display_frames(self.buffer, duration_time, forever_flag, frames_number)

    def clear_display(self):
        # Reset the buffer to turn all LEDs off
        self.buffer = [0xff] * 64
        self.matrix.display_frames(self.buffer, 1000, 1, 1)