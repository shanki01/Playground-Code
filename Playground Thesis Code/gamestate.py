import time

class GameState:
    def __init__(self, coder_mac=None, sequence=None):
        """
        Initialize the game state with position-based player tracking.
        
        Args:
            coder_mac: MAC address of coder device
            sequence: Optional initial game sequence
        """
        self.coder_mac = coder_mac # THE ACTIVE CODER
        self.coders_list = {}
        self.sequence = sequence if sequence else []
        # Initialize player positions with None values
        self.players = {
            1: {"mac": None, "progress": 0, "last_connection": None},
            2: {"mac": None, "progress": 0, "last_connection": None},
            3: {"mac": None, "progress": 0, "last_connection": None},
            4: {"mac": None, "progress": 0, "last_connection": None}
        }
        self.state = "SETUP" # "ACTIVE" "COMPLETED"
        
    def set_sequence(self, sequence):
        """
        Set the game sequence.
        
        Args:
            sequence: List of numbers between 1 and 10
        
        Raises:
            ValueError: If sequence contains invalid numbers
        """
        if all(1 <= num <= 10 for num in sequence):
            self.sequence = sequence
            print(f"Game sequence set to: {self.sequence}")
        else:
            raise ValueError("Sequence must be a list of numbers between 1 and 10.")
    
    
    
    def add_coder_to_list(self, mac_address):
        
        position = self.get_player_position(mac_address)
        if position is not None:
            self.remove_player(position)
        self.coders_list[mac_address] = time.ticks_ms()
        
    def remove_coder_from_list(self, mac_address):
        if mac_address in self.coders_list:
            self.coders_list.pop(mac_address)
            
        
    
    def add_player(self, mac_address, position): # added position
        """
        Add a player at a specific position.
        
        Args:
            mac_address: Player's device MAC address
            position: Position number (1-4)
        
        Returns:
            bool: True if player was added, False if position is occupied
        """
        
        if position not in self.players:
            print(f"Invalid position: {position}. Must be between 1 and 4.")
            return False
            
        if self.players[position]["mac"] is not None:
            print(f"Position {position} is already occupied.")
            return False
            
        self.players[position] = {
            "mac": mac_address,
            "progress": 0,
            "last_connection": time.ticks_ms()
        }
        self.remove_coder_from_list(mac_address) 
        print(f"Player {mac_address} added at position {position}")
        return True
    
    def player_count(self):
        count = 0
        for position, player_data in self.players.items():
              if self.players[position]["mac"] is not None:
                  count = count + 1
        return count               
                    

    def remove_player_by_mac(self, mac): # now by position instead of mac
        """
        Remove a player from a specific position.
        
        Args:
            position: Position number (1-4)
        """
        position = self.get_player_position(mac)
        if position is not None:
            self.players[position] = {
                "mac": None, 
                "progress": 0, 
                "last_connection": None
            }
            print(f"Player at position {position} removed.")
        else:
            print(f"Not player: {mac}") 
    
    def remove_player(self, position): # now by position instead of mac
        """
        Remove a player from a specific position.
        
        Args:
            position: Position number (1-4)
        """
        if position in self.players:
            self.players[position] = {
                "mac": None, 
                "progress": 0, 
                "last_connection": None
            }
            print(f"Player at position {position} removed.")
        else:
            print(f"Invalid position: {position}")            
            
    def update_progress(self, mac_address, step):
        """
        Update progress for a player with given MAC address.
        
        Args:
            mac_address: Player's device MAC address
            step: Current progress step (0-8)
        """
        for position, player in self.players.items():
            if player["mac"] == mac_address:
                player["progress"] = min(step, 8)
                player["last_connection"] = time.ticks_ms()
                print(f"Player at position {position} progress updated to step {step}.")
                return
        print(f"Player {mac_address} not found.")

    def update_connection(self, mac_address):
        """
        Update last connection time for a player.
        
        Args:
            mac_address: Player's device MAC address
        """
        for player in self.players.values():
            if player["mac"] == mac_address:
                player["last_connection"] = time.ticks_ms()
                return
            
    def get_player_position(self, mac_address):
        """
        Get position number for a given MAC address.
        
        Args:
            mac_address: Player's device MAC address
        
        Returns:
            int: Position number (1-4) or None if not found
        """
        for position, player in self.players.items():
            if player["mac"] == mac_address:
                return position
        return None
    
    
    def get_position_status(self, position):
        """
        Get status of a position.
        
        Args:
            position: Position number (1-4)
        
        Returns:
            dict: Player data for the position or None if invalid position
        """
        return self.players.get(position)
    
#     def get_player_progress(self, mac_address):
#         """Get the progress of a specific player."""
#         return self.players.get(mac_address, None)
# 
#     def get_all_progress(self):
#         """Get progress for all players."""
#         return self.players

    def reset_game(self):
        """
        Reset the game state for a NEW GAME
        All players are removed.
        The sequence is deleted.
        
        """
        
        for position in self.players:
            self.players[position] = {
                "mac": None,
                "progress": 0,
                "last_connection": None
            }
        self.sequence = []
        print("Game has been reset. Players removed.")

    def to_dict(self):
            """
            Convert game state to dictionary for saving.
            
            Returns:
                dict: Game state data
            """
            return {
                "coder_mac": self.coder_mac,
                "sequence": self.sequence,
                "players": self.players
            }
        
    def from_dict(self, data):
        """
        Restore game state from dictionary.
        
        Args:
            data: Dictionary containing game state data
        """
        self.coder_mac = data.get("coder_mac")
        self.sequence = data.get("sequence", [])
        self.players = data.get("players", {})
            
    #     def reset_player_activity(self, mac_address):
    #         """Reset the activity timestamp for a player."""
    #         self.players[mac_address] = time.time()

    def remove_inactive_players(self, timeout=600000):
        """
        Remove players who have been inactive for the specified timeout duration.

        Args:
            timeout: time elasped to be considered inactive, default 600000ms (10 minutes)
        """
        
        current_time = time.ticks_ms()
        
        for position, player in self.players.items():
            if time.ticks_diff(player["last_connection"], current_time) > timeout:
                self.remove_player(position)
                    

# Example Usage
if __name__ == "__main__":
    # Initialize the game with a coder's MAC address
    coder_mac = b'\x24\x0A\xC4\xDE\xAD\xBE'
    game = GameState(coder_mac)

    # Set the game sequence
    game.set_sequence([1, 5, 7, 2, 9, 4, 3, 6])

    # Add players dynamically
    player1 = b'\x24\x0A\xC4\x12\x34\x56'
    player2 = b'\x24\x0A\xC4\x65\x43\x21'
    game.add_player(player1)
    game.add_player(player2)

    # Update player progress
    game.update_progress(player1, 3)
    game.update_progress(player2, 5)

    # Display progress
    print(game.get_all_progress())

    # Remove a player
    game.remove_player(player1)

    # Display progress after removal
    print(game.get_all_progress())

    # Reset the game
    game.reset_game()