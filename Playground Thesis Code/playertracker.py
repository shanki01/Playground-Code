from machine import Pin, Timer
import neopixel

colors = {
        0: (0,0,0), #off
        1:(255,0,0), #red
        2:(255,127,0), #orange
        3:(255,255,0), #yellow
        4:(0,255,0), #green
        5:(0,255,255), #cyan
        6:(0,0,255), #blue
        7:(50,0,255), #purple
        8:(150,70,200), #pink
        }

    # Button LED status colors
BUTTON_STATES = {
        'unassigned': (0, 0, 0),      # off
        'requesting': (0, 0, 255),   # blue
        'connected': (0, 125, 125),      # teal
        'completed': (0, 255, 0),   # green
        'disconnected': (125, 125, 0),   # yellow
    }
       
    
    
class PlayerTracker:
    def __init__(self, pin, num_rows=5, row_length=8, init_skip=1, row_skip=4, buttons=5):
        """
        Initialize the NeoPixel player tracker.

        :param pin: GPIO pin connected to the NeoPixels.
        :param num_rows: Number of rows (default is 5: 1 for coder + 4 for players).
        :param row_length: Number of LEDs per row (default is 8).
        """
        self.init_skip = init_skip
        self.buttons = buttons
        self.row_skip = row_skip
        self.num_rows = num_rows
        self.row_length = row_length
        self.total_leds = num_rows * (row_length+row_skip)-row_skip+init_skip+buttons
        
            
        self.np = neopixel.NeoPixel(Pin(pin), self.total_leds)
        self.clear_all()
        self.COLOR_MAP = self.generate_color_map()
        
        self.timer = Timer(2)  # Initialize timer for animations
        self.current_animation = None  # Track current animation state
        
    def start_countdown(self, row_index: int, total_time_ms: int, color=(255, 255, 0)):
        """
        Start a countdown animation on a row of NeoPixels.
        
        Args:
            row_index: Row to animate (4 for coder, 0-3 for players)
            total_time_ms: Total time for countdown in milliseconds
            color: Color for the countdown pixels
        """
        if row_index < 0 or row_index >= self.num_rows:
            print(f"Invalid row index: {row_index}")
            return

        # Calculate timing
        tick_time = total_time_ms // (self.row_length+1)  # Time per pixel
        
        # Set up animation state
        self.current_animation = {
            'row_start': (row_index) * (self.row_length + self.row_skip) + self.init_skip,
            'pixels_left': self.row_length,
            'color': color,
            'row_index': row_index
        }

        # Light up full row initially
        row_start = self.current_animation['row_start']
        row_end = row_start+self.row_length 
        for i in range(self.row_length):
            self.np[row_start + i] = color
        self.np.write()

        # Start timer for animation ticks
        def animation_tick(t):
            if self.current_animation is None:
                t.deinit()
                return
                
            if self.current_animation['pixels_left'] > 0:
                # Turn off next pixel
                pixel_index = (self.row_length - self.current_animation['pixels_left'])
                self.np[self.current_animation['row_start'] + self.row_length - pixel_index] = (0, 0, 0)
                self.np.write()
                self.current_animation['pixels_left'] -= 1
            else:
                # Animation complete
                t.deinit()
                self.current_animation = None
                self.clear_player_progress(row_index)  # Ensure row is clear

        self.timer.init(period=tick_time, mode=Timer.PERIODIC, callback=animation_tick)

    def stop_countdown(self):
        """Stop any current countdown animation."""
        if self.current_animation:
            self.timer.deinit()
            # Clear the animated row
            self.clear_player_progress(self.current_animation['row_index'])
            self.current_animation = None

    def set_button_led(self, position, button_state):
        """
        Set button LED color. Buttons are at end of chain in reverse order.
        
        Args:
            position: Button position (0=coder, 1-4=players)
            button_state: from BUTTON_STATES
        """
        if 0 <= position <= 4:
            if button_state in BUTTON_STATES:
            # Calculate actual LED position
                color = BUTTON_STATES[button_state]
                
                base_index = self.total_leds - self.buttons  # Start of button section
                if position == 0:
                    led_index = self.total_leds - 1  # Coder is last LED
                else:
                    led_index = base_index + (4 - position)  # Players are reversed 4,3,2,1
                print("setting button color", color, "at", led_index)
                self.np[led_index] = color
                self.np.write()
            
    
    def clear_all(self):
        """Clear all LEDs."""
        self.np.fill((0, 0, 0))
        self.np.write()

    def color_wheel(self, pos):
        """
        Generate rainbow colors across 0-255 positions for NeoPixel.
        
        :param pos: Position (0-255) for color generation.
        """
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)
    
    def generate_color_map(self):
        """
        Generate a color map for values 1 to 9 using the color wheel.
        """
        #Colors are G,R,B
        color_map={}
        for __, (k, c) in enumerate(colors.items()):
            color_map[k] = (c[1], c[0], c[2])
        #color_map = colors        #color_map[10] = (255, 255, 255)  # White for 10
        color_map[None] = (0, 0, 0)      # Black (off) for None
        return color_map

    def display_coder_sequence(self, sequence):
        """
        Display the coder's sequence in the last row of LEDs.

        :param sequence: List of 8 numbers representing the sequence.
        """
        coder_start_position = (4) * (self.row_length+self.row_skip)+self.init_skip
        for i, num in enumerate(sequence[:self.row_length]):
            color = self.COLOR_MAP.get(num, (0, 0, 0))
            self.np[i+coder_start_position] = color
        self.np.write()
    
    def update_player_progress(self, player_index, progress, sequence):
        """
        Update the progress lights for a specific player.

        :param player_index: Index of the player (0 to 3).
        :param progress: Number of steps completed (0 to 8).
        :param sequence: The game sequence to determine the color for each step.
        """
        if player_index < 0 or player_index >= (self.num_rows-1):
            print(f"Invalid player index: {player_index}. Must be between 0 and 4.")
            return

        row_start = (player_index) * (self.row_length+self.row_skip)+self.init_skip
        for i in range(self.row_length):
            if i < progress:
                color = self.COLOR_MAP.get(sequence[i], (0, 0, 0))
                self.np[row_start + i] = color
            else:
                self.np[row_start + i] = (0, 0, 0)  # Black for incomplete steps

        self.np.write()

    def clear_player_progress(self, player_index):
        """
        Clear the progress lights for a specific player.

        :param player_index: Index of the player (0 to 4).
        """
        if player_index < 0 or player_index > (self.num_rows - 1):
            print(f"Invalid player index: {player_index}. Must be between 0 and 4.")
            return

        row_start = (player_index) * (self.row_length+self.row_skip)+self.init_skip

        for i in range(self.row_length):
            self.np[row_start + i] = (0, 0, 0)

        self.np.write()
    
    def reset_all_progress(self):
        """Clear the progress lights for all players."""
        for i in range(self.num_rows):
            self.clear_player_progress(i)
        print("All player progress reset.")

    def indicate_request(self, player_index, color=(255, 255, 0)):
        """
        Light up a row of LEDs to indicate an active request.
        
        :param row: The row to light up (4 for coder, 0-3 for players).
        :param color: The color to display (default is yellow).
        """
        if player_index < 0 or player_index >= self.num_rows:
            print(f"Invalid row index: {row}. Must be between 0 and {self.num_rows - 1}.")
            return
        
        row_start = (player_index) * (self.row_length+self.row_skip)+self.init_skip

        for i in range(self.row_length):
            self.np[row_start + i] = color
        self.np.write()