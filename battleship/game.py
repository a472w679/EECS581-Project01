# Filename: game.py
# Description: This module defines the Game class, which handles the game logic, phases (menu, ship placement, attack), and player turns for the Battleship game.
# Inputs: None
# Output: Controls game flow, manages turns, handles board rendering, and manages user input (ship placement and attacks).
# Other sources for the code: ChatGPT (for proper commenting)
# Authors: Xavier and Andrew
# Creation Date: 9th of September, 2024

from pyray import *             # Import necessary functions from pyray for window and input handling.
from .renderer import Renderer  # Import the Renderer class for drawing the game board and window.
from .player import Player      # Import the Player class that manages player-specific actions and state.
from .constants import *        # Import necessary game constants like cell size, colors, etc.
from .board import Orientation  # Import Orientation enum for ship orientation.
from .player import Powerup     # Import Powerup enum for powerup selection.
import random                   # Import random module for AI functionality

class Game:
    def __init__(self):
        # Initialize game information
        self.turn = 1                                       # Indicates whose turn it is (1 for Player 1, 2 for Player 2/AI).
        self.turn_count = 0                                 # Number of completed turns
        self.player1 = Player(1)                            # Create Player 1.
        self.player2 = Player(2)                            # Create Player 2 (or AI).
        self.show_own_board = False                         # Tracks whether the player is viewing their own board.
        self.is_ai = None                                   # Initialize to None, will be set when player selects game mode
        self.ai_level = None                                # Initialize to None, set to -1 for PvP, 0-2 for AI levels
        self.ai_hard_last_hit = [0,0]                       # Cell that hard AI last hit, begins search from here
        self.ship_orientation = Orientation.HORIZONTAL      # Set initial ship orientation to horizontal.
        self.player_name = {1: "Player", 2: "Player 2"}     # Default names for PvP mode
        self.powerup_selection_phase = False                # Flag for powerup selection phase
        self.preview_cells = []                             # Store cells to be previewed

        # Utility lookup tables for player and enemy references
        self.player_lookup_table = {1: self.player1, 2: self.player2}   # Maps turn number to the current player.
        self.enemy_lookup_table = {1: self.player2, 2: self.player1}    # Maps turn number to the enemy player.

        # Game phase states
        self.menu_phase = True              # Start the game in the menu phase.
        self.mode_selection_phase = True    # Phase for selecting game mode
        self.ship_selection_phase = False   # Phase for selecting number of ships
        self.place_ship_phase = False       # Ship placement phase will activate after the menu.
        self.attack_phase = False           # Attack phase will activate once both players have placed their ships.
        self.game_end_phase = False         # Game end phase will show the board that lost and their sunk ships

        # Game messages to display during different phases
        self.message = ""                                               # Used later for player turn information
        self.title = "Select Game Type, Then Type Ship Amount (1-5)"    # Initial message for the ship selection phase.
        self.win_message = ""                                           # The message to display when a player wins.
        self.last_move_message = ""                                     # Message for showing the result of the last move (hit/miss).
        self.secondary_message = ""                                     # Secondary message for additional information.
        self.color_info = SHIP_COLOR_INFO                               # Display ship color legend/info.

    def get_placement(self, player):
        '''
        Handles ship placement for a player.
        Args:
            player: The player placing their ships.
        '''
        i, j = Renderer.get_mouse_board_coordinates()               # Get mouse cursor coordinates on the board.

        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):  # Check if the left mouse button was clicked.
            res = player.place_ship(i, j, player.ships[-1],
                                    self.ship_orientation)          # Attempt to place the player's last remaining ship at the coordinates.
            if not res:
                self.last_move_message = "Not a correct placement!"  # If the placement failed, show an error message.
            else:
                self.last_move_message = ""                         # Reset the last move message.
                player.ships.pop()                                  # Remove the placed ship from the player's list.

        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_RIGHT):  # Check if right mouse button was clicked.
            if (self.ship_orientation is Orientation.HORIZONTAL):   # Check if orientation is currently horizontal
                self.ship_orientation = Orientation.VERTICAL        # If horizontal, go vertical
            else:
                self.ship_orientation = Orientation.HORIZONTAL  # Otherwise, go horizontal (flip)

        # If all ships have been placed, mark the player as finished placing ships.
        if not player.ships:
            player.ships_placed = True

    def get_attack(self, player, enemy):
        '''
        Handles player attacks on the enemy's board.
        Args:
            player: The attacking player.
            enemy: The enemy player whose board is being attacked.
        Returns:
            True if an attack occurred, otherwise False.
        '''
        # Get the cell coordinates under the mouse cursor
        i, j = Renderer.get_mouse_board_coordinates()

        # Handle Line Shot rotation
        key = get_key_pressed()
        if key == ord('r') and player.powerup_options and player.powerup_options[player.powerup_choice] == Powerup.LINE_SHOT:
            # Toggle the line shot orientation between horizontal and vertical
            player.orientation = (Orientation.VERTICAL 
                if player.orientation == Orientation.HORIZONTAL 
                else Orientation.HORIZONTAL)
            
        # Update preview cells based on current mouse position and active powerup
        self.preview_cells = player.get_preview_cells(i, j, enemy.board)

        if self.is_ai and self.turn == 2:                           # If it's the AI's turn
            return self.get_ai_attack(player, enemy)                # Use AI attack logic
        i, j = Renderer.get_mouse_board_coordinates()               # Get mouse cursor coordinates on the enemy's board.
        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):  # Check if the left mouse button was clicked.
            if enemy.board.is_valid_cell(i, j):                     # Ensure the clicked cell is valid for an attack.
                return self.process_attack(player, enemy, i, j)     # Process the attack

        return False

    def get_ai_attack(self, player, enemy):
        '''
        Handles AI attacks on the player's board.
        Args:
            player: The AI player.
            enemy: The human player whose board is being attacked.
        Returns:
            True if an attack occurred, otherwise False.
        '''

        invalid_cell_types = [HIT_CELL, MISS_CELL, SUNK_CELL]

        # Easy AI: Random attack
        if self.ai_level == 0:
            i, j = random.randint(0, 9), random.randint(0, 9)  # Generate random coordinates
            while not enemy.board.is_valid_cell(i, j) or enemy.board.cells[i][j] in invalid_cell_types:
                i, j = random.randint(0, 9), random.randint(0,9)  # Generate new coordinates if invalid or already attacked

        # Medium AI: Random attack, or attack orthogonally to hit cell
        elif self.ai_level == 1:
            i, j = 0, 0  # Placeholder
            found_cell = False  # Whether a cell to hit has been found or not
            for row in range(10):
                for col in range(10):
                    if enemy.board.cells[row][col] == HIT_CELL:  # If the cell has been hit, not sunk
                        for offsetX in range(-1,2):  # X offset from left (-1) to right (1)
                            for offsetY in range(-1,2):  # Y offset from left (-1) to right (1)
                                if (offsetX + offsetY) % 2 == 0:  # If the cell is not orthogonal in one direction, skip cell
                                    continue
                                # Check bounds of board
                                if not enemy.board.is_valid_cell(row + offsetY, col + offsetX):
                                    continue
                                # In the case of a multishot attack, don't hit the same cell twice
                                if (row + offsetY, col + offsetX) in player.multishot_coords:
                                    continue
                                if enemy.board.cells[row + offsetY][col + offsetX] not in invalid_cell_types:  # If cell is not invalid
                                    found_cell = True  # Cell has been found
                                    i, j = row + offsetY, col + offsetX  # Mark coordinates to hit
                                    break
                            # Break out of loop
                            if found_cell: break
                    if found_cell: break
                if found_cell: break


            # Hit cell not found, attack randomly
            if not found_cell:
                i, j = random.randint(0, 9), random.randint(0, 9)  # Generate random coordinates
                while not enemy.board.is_valid_cell(i, j) or enemy.board.cells[i][j] in invalid_cell_types or (i, j) in player.multishot_coords:
                    # In the case of a multishot attack, don't hit the same cell twice
                    i, j = random.randint(0, 9), random.randint(0,9)  # Generate new coordinates if invalid or already attacked

        # Hard AI: Attack ship every turn
        elif self.ai_level == 2:
            found_cell = False
            i, j = 0, 0  # Initialize coordinates
            for row in range(10):  # Loop through rows, starting from last hit
                for col in range(10):  # Loop through cols, starting from last hit
                    if enemy.board.cells[row][col] > 0:  # If the cell is a valid hit
                        if (row, col) in player.multishot_coords:
                            continue
                        i, j = row, col  # Set current row and col as coords to attack
                        found_cell = True
                        break
                if found_cell:  # Hit has been found, break out of loop
                    break
            # No cell was found that hasn't already been hit.
            # Probably a multishot situation. Just hit brand new empty cells
            if not found_cell:
                for row in range(10):
                    for col in range(10):
                        if (row, col) not in player.multishot_coords:
                            i, j = row, col
                            break

        print("attacked: " + str(i) + "," + str(j))
        return self.process_attack(player, enemy, i, j)  # Process the AI's attack

    def process_attack(self, player, enemy, i, j):
        '''
        Processes an attack on the enemy's board.
        Args:
            player: The attacking player.
            enemy: The enemy player whose board is being attacked.
            i, j: The coordinates of the attack.
        Returns:
            True if the attack was valid, otherwise False.
        '''

        # Respecting powerups, get the coordinates that are attacked as a result of this click
        shots = player.get_shots_from_attack(i, j, enemy.board)
        if shots is None:  # Multishot powerup may not finish in one click
            return False

        hits = 0
        sinks = 0
        for shot in shots:
            res, ship_size = enemy.place_attack(shot[0], shot[1])  # Perform the attack on the enemy's board.
            if res:
                hits += 1
            if res and enemy.ship_count[ship_size] == 0:
                sinks += 1

        # Report number of hits and sinks to opponent with the last move message
        self.last_move_message = f"{self.player_name[player.num]} has hit {hits} ship cells"  # Notifies the player of a miss.
        if sinks > 0:
            self.last_move_message += f", sinking {sinks} ships"

        return True

    def show_menu(self):
        '''
        Displays the initial menu where players choose how many ships to use and game mode.
        '''
        if self.ai_level is None:  # If game mode hasn't been selected yet
            new_ai_level = Renderer.draw_ai_buttons(self.ai_level)
            if new_ai_level != self.ai_level:
                self.ai_level = new_ai_level
                if self.ai_level == -1:  # PvP mode
                    self.is_ai = False
                    self.player_name[2] = "Player 2"
                else:  # AI mode
                    self.is_ai = True
                    self.player_name[2] = f"{'Easy' if self.ai_level == 0 else 'AI'} AI"
            return  # Wait for player to select game mode

        key = get_key_pressed() - ASCII_0                                   # Get the key the user pressed and adjust it to a numeric value.
        if key > 0 and key <= 5:                                            # Ensure the ship count is between 1 and 5.
            self.player1.get_ships(key)                                     # Give Player 1 the specified number of ships.
            self.player2.get_ships(key)                                     # Give Player 2 the same number of ships.
            self.message = f"{self.player_name[1]}'s Turn to Place Ships"   # Update the message to indicate the next phase.
            self.menu_phase = False                                         # Exit the menu phase.
            self.place_ship_phase = True                                    # Enter the ship placement phase.
            self.title = ""                                                 # Remove title line from the screen

            if self.is_ai:
                self.place_ai_ships()  # Place AI ships randomly

    def place_ai_ships(self):
        '''
        Randomly places ships for the AI player.
        '''
        for ship_size in self.player2.ships[:]:
            placed = False
            while not placed:
                i = random.randint(0, 9)
                j = random.randint(0, 9)
                orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
                if self.player2.board.is_placeable_on(i, j, ship_size, orientation):
                    self.player2.place_ship(i, j, ship_size, orientation)
                    placed = True
            self.player2.ships.remove(ship_size)
        self.player2.ships_placed = True

    def show_place_ship_phase(self):
        '''
        Manages the ship placement phase.
        '''
        current_player = self.player_lookup_table[self.turn]  # Get current player
        Renderer.draw_board(current_player.board, False, current_player.ships[-1] if current_player.ships else 1,
                            self.ship_orientation)  # Draw the current player's board.

        if not self.is_ai or (self.is_ai and self.turn == 1):
            self.get_placement(current_player)                             # Handle ship placement for the current player.

        if self.player1.ships_placed:                                      # If Player 1 has placed all ships:
            self.message = f"{self.player_name[2]}'s Turn to Place Ships"  # Update the message for Player 2's/AI's turn.
            self.turn = 2                                                  # Switch the turn to Player 2/AI.
        else:
            self.turn = 1                                                  # Otherwise, it's still Player 1's turn.

        if self.player1.ships_placed and self.player2.ships_placed:         # Once both players have placed all ships:
            self.place_ship_phase = False                                   # Exit the ship placement phase.
            self.attack_phase = True                                        # Enter the attack phase.
            self.secondary_message = "Viewing ENEMY'S Board [B to Switch]"  # Display instruction for viewing the player's own board.

    def toggle_show_board(self):
        '''
        Toggles the display between the player's own board and the enemy's board.
        '''
        key = get_key_pressed()                                                 # Get the key pressed by the user.
        if key == ASCII_B:                                                      # If the user presses the 'B' key:
            if self.show_own_board:                                             # If the player is currently viewing their own board:
                self.secondary_message = "Viewing ENEMY'S Board [B to Switch]"  # Update the message for viewing the enemy board.
                self.show_own_board = False                                     # Switch to viewing the enemy board.
            else:
                self.secondary_message = "Viewing OWN Board [B to Switch]"  # Update the message for viewing own board.
                self.show_own_board = True                                  # Switch to viewing own board.

    def show_attack_phase(self):
        '''
        Manages the attack phase where players take turns attacking each other.
        '''
        self.toggle_show_board()                                            # Toggle the board view between the player's own and enemy's board.
        self.message = f"{self.player_name[self.turn]}'s Turn to Attack"    # Update the message to indicate whose turn it is.

        current_player = self.player_lookup_table[self.turn]                # Get the current attacking player.
        current_enemy_player = self.enemy_lookup_table[self.turn]           # Get the current enemy player.
        if self.show_own_board:
            Renderer.draw_board(current_player.board, False)                # Draw the current player's own board.
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                self.last_move_message = "Can't attack! Currently viewing own board!"  # If viewing own board, disallow attacks.
        else:
            Renderer.draw_board(current_enemy_player.board, True, preview_cells=self.preview_cells)               # Draw the enemy player's board.
            res = self.get_attack(current_player, current_enemy_player)         # Perform an attack if allowed.
            if current_enemy_player.is_loss():                                  # Check if the enemy has lost all their ships.
                self.message = ""                                               # Remove message from the UI.
                self.last_move_message = ""                                     # Remove the last move message from UI.
                self.secondary_message = ""                                     # Remove the secondary message from UI.
                self.win_message = f"{self.player_name[self.turn]} Has Won!"    # Declare the winner.
                self.attack_phase = False                                       # End the attack phase.
                self.game_end_phase = True                                      # Set phase to game end
                return

            if res:
                self.turn = 3 - self.turn   # Switch turns (1 becomes 2, 2 becomes 1)
                self.turn_count += 1        # Count this turn as done

                # Give the opponent powerup choices every fourth turn
                if (self.turn_count // 2) % 4 == 3:
                    current_enemy_player.get_new_powerup_options()
                else:
                    current_enemy_player.powerup_options = []

                # Enemy will start with the top powerup choice selected
                current_enemy_player.powerup_choice = 0

    def show_game_end_phase(self):
        losing_player = self.enemy_lookup_table[self.turn]
        Renderer.draw_board(losing_player.board, True)

    def draw_info_messages(self):
        '''
        Draws informational messages below the game board.
        '''
        turn_message_color = BLUE if self.turn == 1 else GREEN
        Renderer.draw_font_text(self.message, BOARD_PADDING_LEFT, 34, 22, turn_message_color)               # draw turn-based message
        Renderer.draw_font_text(self.title, 70, 175, 30, BLACK)                                             # Draw the main message.
        Renderer.draw_font_text(self.win_message, 235, 370, 30, turn_message_color)                         # Draw the win message.
        Renderer.draw_font_text(self.last_move_message, BOARD_PADDING_LEFT, 370, 20, RED)                   # Draw the last move message.
        Renderer.draw_font_text(self.secondary_message, BOARD_PADDING_LEFT, 395, 20, turn_message_color)    # Draw any secondary messages.
        Renderer.draw_font_text(self.color_info, 10, 10, 15, BLACK)                                         # Draw the ship color legend/info.

        player = self.player_lookup_table[self.turn] # The player currently playing
        if self.place_ship_phase:
            if not self.is_ai or (self.is_ai and self.turn == 1):
                Renderer.draw_remaining_ships_to_place(player)
        elif self.menu_phase:
            new_ai_level = Renderer.draw_ai_buttons(self.ai_level)
            if new_ai_level != self.ai_level:
                self.ai_level = new_ai_level
                self.is_ai = (self.ai_level > -1) # -1 in the case of PvP
                if self.is_ai:
                    # Update name for AI
                    if self.ai_level == 0:
                        self.player_name[2] = "Easy AI"
                    if self.ai_level == 1:
                        self.player_name[2] = "Medium AI"
                    if self.ai_level == 2:
                        self.player_name[2] = "Hard AI"
                else:
                    self.player_name[2] = "Player 2"  # Reset name for PvP mode

        # When the powerup_options list is not empty, the player can choose one of them.
        # Draw the powerup selection buttons.
        elif self.attack_phase and player.powerup_options and not player.powerup_locked:
            # Gets the text to be printed for any specific powerup
            label_map = {
                Powerup.MULTISHOT: "Multishot",
                Powerup.BIG_SHOT: "Big shot",
                Powerup.LINE_SHOT: "Line shot",
                Powerup.RANDOM_SHOT: "Random shots",
                Powerup.REVEAL_SHOT: "Reveal area",
                }
            # Set the player's powerup choice based on which button they have selected
            player.powerup_choice = Renderer.draw_powerup_buttons(
                    player.powerup_choice,
                    label_map[player.powerup_options[0]],
                    label_map[player.powerup_options[1]]
            )

    def game_loop(self):
        '''
        The main game loop. This function is continuously called to update the game state.
        '''
        self.draw_info_messages()           # Draw the game messages.
        if self.menu_phase:
            self.show_menu()                # Show the menu phase.
        elif self.place_ship_phase:
            self.show_place_ship_phase()    # Show the ship placement phase.
        elif self.attack_phase:
            self.show_attack_phase()        # Show the attack phase.
        elif self.game_end_phase:
            self.show_game_end_phase()
