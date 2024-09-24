# Filename: game.py
# Description: This module defines the Game class, which handles the game logic, phases (menu, ship placement, attack), and player turns for the Battleship game.
# Inputs: None
# Output: Controls game flow, manages turns, handles board rendering, and manages user input (ship placement and attacks).
# Other sources for the code: ChatGPT (for proper commenting)
# Authors: Xavier and Andrew
# Creation Date: 9th of September, 2024

from pyray import *  # Import necessary functions from pyray for window and input handling.
from .renderer import Renderer  # Import the Renderer class for drawing the game board and window.
from .player import Player  # Import the Player class that manages player-specific actions and state.
from .constants import *  # Import necessary game constants like cell size, colors, etc.
from .board import Orientation # Import Orientation enum for ship orientation.

class Game:
    def __init__(self):
        # Initialize game information
        self.turn = 1  # Indicates whose turn it is (1 for Player 1, 2 for Player 2).
        self.player1 = Player(1)  # Create Player 1.
        self.player2 = Player(2)  # Create Player 2.
        self.show_own_board = False  # Tracks whether the player is viewing their own board.
        self.is_ai = False # PvP or vs-AI
        self.ai_level = -1 # Tracks whether the ai is easy AI (0), medium AI (1), or hard AI (2). Otherwise (-1)
        self.ship_orientation = Orientation.HORIZONTAL # Set intial ship orientation to horizontal.

        # Utility lookup tables for player and enemy references
        self.player_lookup_table = {1: self.player1, 2: self.player2}  # Maps turn number to the current player.
        self.enemy_lookup_table = {1: self.player2, 2: self.player1}  # Maps turn number to the enemy player.

        # Game phase states
        self.menu_phase = True  # Start the game in the menu phase.
        self.place_ship_phase = False  # Ship placement phase will activate after the menu.
        self.attack_phase = False  # Attack phase will activate once both players have placed their ships.
        self.game_end_phase = False # Game end phase will show the board that lost and their sunk ships 

        # Game messages to display during different phases
        self.message = "" # Used later for player turn information
        self.title = "Enter Ship Number to Play with (Min: 1, Max: 5)"  # Initial message for the ship selection phase.
        self.win_message = "" # The message to display when a player wins.
        self.last_move_message = ""  # Message for showing the result of the last move (hit/miss).
        self.secondary_message = ""  # Secondary message for additional information.
        self.color_info = SHIP_COLOR_INFO  # Display ship color legend/info.

    def get_placement(self, player):
        '''
        Handles ship placement for a player.
        Args:
            player: The player placing their ships.
        '''
        i, j = Renderer.get_mouse_board_coordinates()  # Get mouse cursor coordinates on the board.

        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):  # Check if the left mouse button was clicked.
            res = player.place_ship(i, j, player.ships[-1], self.ship_orientation)  # Attempt to place the player's last remaining ship at the coordinates.
            if not res:
                self.last_move_message = "Not a correct placement!"  # If the placement failed, show an error message.
            else:
                self.last_move_message = "" # Reset the last move message.
                player.ships.pop()  # Remove the placed ship from the player's list.
        
        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_RIGHT): # Check if right mouse button was clicked.
            if (self.ship_orientation is Orientation.HORIZONTAL): # Check if orientation is currently horizontal
                self.ship_orientation = Orientation.VERTICAL # If horizontal, go vertical
            else:
                self.ship_orientation = Orientation.HORIZONTAL # Otherwise, go horizontal (flip)

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
        i, j = Renderer.get_mouse_board_coordinates()  # Get mouse cursor coordinates on the enemy's board.
        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):  # Check if the left mouse button was clicked.
            if enemy.board.is_valid_cell(i, j):  # Ensure the clicked cell is valid for an attack.
                res, ship_size = enemy.place_attack(i, j)  # Perform the attack on the enemy's board.
                if ship_size == MISS_CELL: # player chose a cell they already missed/hit/sunk  
                    self.last_move_message = f"Player {player.num} already shot as this cell!"
                    return False 

                if res and enemy.ship_count[ship_size] == 0: 
                    self.last_move_message = f"Player {player.num} has sunk a ship!"  # Notifys the player that they sunk a ship.
                elif res:
                    self.last_move_message = f"Player {player.num} has hit a ship!"  # Notifys the player of a successful hit.
                else:
                    self.last_move_message = f"Player {player.num} has missed!"  # Notifys the player of a miss.
                coord = chr(ord("A") + i) + str(j+1)
                self.last_move_message += " " + coord

                return True

        return False

    def show_menu(self):
        '''
        Displays the initial menu where players choose how many ships to use.
        '''
        key = get_key_pressed() - ASCII_0  # Get the key the user pressed and adjust it to a numeric value.
        if key > 0 and key <= 5:  # Ensure the ship count is between 1 and 5.
            self.player1.get_ships(key)  # Give Player 1 the specified number of ships.
            self.player2.get_ships(key)  # Give Player 2 the same number of ships.
            self.message = "Player 1's Turn to Place Ships"  # Update the message to indicate the next phase.
            self.menu_phase = False  # Exit the menu phase.
            self.place_ship_phase = True  # Enter the ship placement phase.
            self.title = "" # Remove title line from the screen

    def show_place_ship_phase(self):
        '''
        Manages the ship placement phase.
        '''
        current_player = self.player_lookup_table[self.turn] # Get current player
        Renderer.draw_board(current_player.board, False, current_player.ships[-1], self.ship_orientation)  # Draw the current player's board.
        self.get_placement(current_player)  # Handle ship placement for the current player.
        if self.player1.ships_placed:  # If Player 1 has placed all ships:
            self.message = "Player 2's Turn to Place Ships"  # Update the message for Player 2's turn.
            self.turn = 2  # Switch the turn to Player 2.
        else:
            self.turn = 1  # Otherwise, it's still Player 1's turn.

        if self.player1.ships_placed and self.player2.ships_placed:  # Once both players have placed all ships:
            self.place_ship_phase = False  # Exit the ship placement phase.
            self.attack_phase = True  # Enter the attack phase.
            self.secondary_message = "Viewing ENEMY'S Board [B to Switch]"  # Display instruction for viewing the player's own board.

    def toggle_show_board(self):
        '''
        Toggles the display between the player's own board and the enemy's board.
        '''
        key = get_key_pressed()  # Get the key pressed by the user.
        if key == ASCII_B:  # If the user presses the 'B' key:
            if self.show_own_board:  # If the player is currently viewing their own board:
                self.secondary_message = "Viewing ENEMY'S Board [B to Switch]"  # Update the message for viewing the enemy board.
                self.show_own_board = False  # Switch to viewing the enemy board.
            else:
                self.secondary_message = "Viewing OWN Board [B to Switch]"  # Update the message for viewing own board.
                self.show_own_board = True  # Switch to viewing own board.

    def show_attack_phase(self):
        '''
        Manages the attack phase where players take turns attacking each other.
        '''
        self.toggle_show_board()  # Toggle the board view between the player's own and enemy's board.
        self.message = f"Player {self.turn}'s Turn to Attack"  # Update the message to indicate whose turn it is.

        current_player = self.player_lookup_table[self.turn]  # Get the current attacking player.
        current_enemy_player = self.enemy_lookup_table[self.turn]  # Get the current enemy player.
        if self.show_own_board:
            Renderer.draw_board(current_player.board, False)  # Draw the current player's own board.
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                self.last_move_message = "Can't attack! Currently viewing own board!"  # If viewing own board, disallow attacks.
        else:
            Renderer.draw_board(current_enemy_player.board, True)  # Draw the enemy player's board.
            res = self.get_attack(current_player, current_enemy_player)  # Perform an attack if allowed.
            if current_enemy_player.is_loss():  # Check if the enemy has lost all their ships.
                self.message = "" # Remove message from the UI.
                self.last_move_message = "" # Remove the last move message from UI.
                self.secondary_message = "" # Remove the secondary message from UI.
                self.win_message = f"Player {self.turn} Has Won!"  # Declare the winner.
                self.attack_phase = False  # End the attack phase.
                self.game_end_phase = True  # Set phase to game end 
                return 

            if res and self.turn == 1:
                self.turn = 2  # Switch turns if Player 1 attacked.
            elif res and self.turn == 2:
                self.turn = 1  # Switch turns if Player 2 attacked.

    def show_game_end_phase(self): 
        losing_player = self.enemy_lookup_table[self.turn]
        Renderer.draw_board(losing_player.board, True)

    def draw_info_messages(self):
        '''
        Draws informational messages below the game board.
        '''
        turn_message_color = BLUE if self.turn == 1 else GREEN
        Renderer.draw_font_text(self.message, BOARD_PADDING_LEFT, 34, 22, turn_message_color) # draw turn-based message
        Renderer.draw_font_text(self.title, 70, 175, 30, BLACK)  # Draw the main message.
        Renderer.draw_font_text(self.win_message, 235, 370, 30, turn_message_color) # Draw the win message.
        Renderer.draw_font_text(self.last_move_message, BOARD_PADDING_LEFT, 370, 20, RED)  # Draw the last move message.
        Renderer.draw_font_text(self.secondary_message, BOARD_PADDING_LEFT, 395, 20, turn_message_color)  # Draw any secondary messages.
        Renderer.draw_font_text(self.color_info, 10, 10, 15, BLACK)  # Draw the ship color legend/info.
        if self.place_ship_phase: 
            Renderer.draw_remaining_ships_to_place(self.player_lookup_table[self.turn])
        elif self.menu_phase:
            self.ai_level = Renderer.draw_ai_buttons(self.ai_level)
            self.is_ai = (self.ai_level > -1)

    def game_loop(self):
        '''
        The main game loop. This function is continuously called to update the game state.
        '''
        self.draw_info_messages()  # Draw the game messages.
        if self.menu_phase:
            self.show_menu()  # Show the menu phase.
        elif self.place_ship_phase:
            self.show_place_ship_phase()  # Show the ship placement phase.
        elif self.attack_phase:
            self.show_attack_phase()  # Show the attack phase.
        elif self.game_end_phase: 
            self.show_game_end_phase()

