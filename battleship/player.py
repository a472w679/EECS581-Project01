# Filename: player.py
# Description: This module defines the Player class for a Battleship game. It manages the player's board, ships, and attacks.
# Inputs: None
# Output: The functionality to place ships, place attacks, and determine if the player has lost
# Other sources for the code: ChatGPT (for proper commenting format)
# Author: Xavier and Andrew
# Creation Date: 9th of September, 2024

from .board import Board  # Importing the Board class from the current package.
from .board import Orientation
from .constants import *  # Importing all constants like HIT_CELL and MISS_CELL used for game logic.

class Player:
    def __init__(self, num):
        """
        Initializes a new Player object.
        - num: The player's number (to distinguish between players).
        - Initializes ships as an empty list.
        - Sets num_ship_cells to track the total number of cells occupied by ships.
        - Initializes the player's board.
        - The ships_placed flag indicates whether all ships have been placed.
        """
        self.num = num  # The player number is stored in the instance variable.
        self.ships = []  # Empty list to hold the player's ships.
        self.num_ship_cells = 0  # Total number of cells occupied by ships, initialized to 0.
        self.board = Board()  # Initializes a new Board instance for the player.
        self.ships_placed = False  # Indicates if ships have been placed, initialized to False.

    def get_ships(self, num):
        """
        Generates ships for the player.
        - num: The number of ships to create.
        - The ships list contains ships from size 1 up to 'num'.
        - Also calculates the total number of ship cells.
        """
        self.ships = [i for i in range(1, num + 1)]  # Create ships with sizes from 1 to 'num'.
        self.num_ship_cells = sum(self.ships)  # Calculate total number of cells that the ships occupy.

    def place_ship(self, i, j, ship_size, orientation = Orientation.HORIZONTAL):
        '''
        Places a ship on the player's board.
        - i: Row index where the ship starts.
        - j: Column index where the ship starts.
        - ship_size: The size of the ship to place.
        - Returns True if the ship is successfully placed, False otherwise.
        '''
        if self.board.is_placeable_on(i, j, ship_size, orientation):  # Check if the ship can be placed at (i, j).
            stepX = orientation == Orientation.HORIZONTAL # X step is 1 if horizontal, 0 otherwise.
            stepY = orientation == Orientation.VERTICAL   # Y step is 1 if vertical  , 0 otherwise.

            # Place the ship by marking the cells occupied by the ship on the board.
            for pos in range(ship_size):
                setX = j + pos * stepX # Calculate the X position to set.
                setY = i + pos * stepY # Calculate the Y position to set.
                self.board.cells[setY][setX] = ship_size  # Mark the cells with the ship size.
            return True  # Ship placement was successful.
        return False  # Ship placement failed.

    def place_attack(self, i, j):
        '''
        Places an attack on the player's board.
        - i: Row index where the attack occurs.
        - j: Column index where the attack occurs.
        - Returns True if the attack hits a ship, False otherwise.
        '''
        if self.board.is_ship(i, j):  # Check if there is a ship at (i, j).
            # Attack hits a ship, mark the cell as a hit.
            self.board.cells[i][j] = HIT_CELL  # Mark the cell with HIT_CELL constant.
            self.num_ship_cells -= 1  # Decrease the count of ship cells after a hit.
            return True  # Attack was a hit.
        else:
            # Attack misses, mark the cell as a miss.
            self.board.cells[i][j] = MISS_CELL  # Mark the cell with MISS_CELL constant.
            return False  # Attack was a miss.

    def is_loss(self):
        """
        Determines if the player has lost the game.
        - A player loses if they have no remaining ship cells (i.e., all ships have been destroyed).
        - Returns True if the player has lost, False otherwise.
        """
        return self.num_ship_cells <= 0  # If no ship cells remain, the player has lost.
