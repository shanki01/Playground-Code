I2C_CMD_DISP_NUM = 0x03

class LEDSequencer:
    def __init__(self, matrix):
        self.matrix = matrix
        self.buffer = [0xff] * 64  # Initialize with all pixels off (black)
        self.c = {
        'red': 0x00,
        'orange': 0x12,
        'yellow': 0x18,
        'green': 0x52,
        'cyan': 0x7f,
        'blue': 0xaa,
        'purple': 0xc3,
        'pink': 0xdc,
        'white': 0xfe,
        'black': 0xff,
        }

    def display_color_pixel(self, color, x, y):
        # Update the buffer at the specified (x, y) position
        index = y * 8 + x
        self.buffer[index] = self.c[color]

        # Display the updated buffer
        duration_time = 1000  # Duration for the display, in milliseconds
        forever_flag = 1      # Display continuously until interrupted
        frames_number = 1     # Single frame

        self.matrix.display_frames(self.buffer, duration_time, forever_flag, frames_number)
    
    def display_number(self, number, color):
        color = self.c[color]
        self.nums = {
            1: [[4,4],[4,5]],
            2: [[3,1],[3,2],[5,5],[5,6]],
            3: [[3,1],[3,2],[5,5],[5,6],[4,3],[4,4]],
            4: [[3,1],[3,2],[5,5],[5,6],[5,1],[5,2],[3,5],[3,6]],
            5: [[3,1],[3,2],[5,5],[5,6],[5,1],[5,2],[3,5],[3,6],[4,3],[4,4]],
            6: [[2,1],[2,2],[4,1],[4,2],[6,1],[6,2],[2,5],[2,6],[4,5],[4,6],[6,5],[6,6]],
            7: [[3,1],[3,2],[5,5],[5,6],[5,1],[5,2],[3,5],[3,6],[4,3],[4,4],[2,3],[2,4],[6,2],[6,4]],
            8: [[2,1],[3,1],[5,1],[6,1],[2,3],[3,3],[5,3],[6,3],[2,5],[3,5],[5,5],[6,5],[2,7],[3,7],[5,7],[6,7]],
            9: [[3,1],[3,2],[5,5],[5,6],[5,1],[5,2],[3,5],[3,6],[4,3],[4,4],[2,3],[2,4],[6,2],[6,4],[5,0],[5,1],[5,6],[5,7]],
            }
        num_data = self.nums[number]
        for point in num_data:
            x = point[0]
            y = point[1]
            self.display_color_pixel(color,x,y)

    def clear_display(self):
        # Reset the buffer to turn all LEDs off
        self.buffer = [0xff] * 64
        self.matrix.display_frames(self.buffer, 1000, 1, 1)