# Filename: board.py
# Description: This module defines the Board class for the Battleship game, which handles the creation of the game board and its operations such as placing ships, validating cells, and checking for ships.
# Inputs: None
# Output: Functionality for managing the game board, including ship placement and attack handling.
# Other sources for the code: ChatGPT(for proper commenting format).
# Authors: Xavier and Andrew
# Creation Date: 9th of September, 2024
from enum import Enum

class Orientation(Enum):
    '''Orientation enumeration for ship orientation'''
    HORIZONTAL = 0 # Ship is horizontal
    VERTICAL   = 1 # Ship is vertical

class Board:
    def __init__(self, rows=10, cols=10):
        '''
        Initializes a Board instance with the specified number of rows and columns.
        Creates a grid (2D list) to represent the game board, where each cell is initialized to -1 (indicating an empty cell).
        Args:
            rows: Number of rows in the board.
            cols: Number of columns in the board.
        '''
        self.rows = rows  # Number of rows on the board.
        self.cols = cols  # Number of columns on the board.
        self.cells = [[-1] * rows for _ in range(cols)]  # Initialize a 2D list of cells, all set to -1 (EMPTY_CELL).

    
    def is_valid_cell(self, i, j):
        '''
        Checks if the specified cell (i, j) is within the valid bounds of the board.
        Args:
            i: Row index of the cell.
            j: Column index of the cell.
        Returns:
            True if the cell is within the board's bounds, otherwise False.
        '''
        return i >= 0 and i < self.rows and j >= 0 and j < self.cols  # Return True if both row and column indices are valid.

    def is_placeable_on(self, i, j, ship_size, orientation = Orientation.HORIZONTAL):
        '''
        Determines if a ship of the given size can be placed at the specified location (i, j).
        Args:
            i: Row index where the ship will be placed.
            j: Starting column index where the ship will be placed.
            ship_size: The size of the ship to be placed.
        Returns:
            True if the ship can be placed on the board at the given position, otherwise False.
        '''
        stepX = orientation == Orientation.HORIZONTAL # X step is 1 if horizontal, 0 otherwise.
        stepY = orientation == Orientation.VERTICAL   # Y step is 1 if vertical  , 0 otherwise.

        # Iterate over the cells the ship will occupy to check if they are empty.
        for x in range(ship_size):
            checkX = j + x * stepX # Calculate the X position to set.
            checkY = i + x * stepY # Calculate the Y position to set.

            if not self.is_valid_cell(checkY, checkX): # Check if current cell is in grid
                return False # Return false if not in grid

            if self.cells[checkY][checkX] != -1:  # If any cell is not empty, return False (ship cannot be placed).
                return False

        return True  # Return True if the ship can be placed successfully.

    def is_ship(self, i, j):
        '''
        Checks if the cell at position (i, j) contains a ship.
        Args:
            i: Row index of the cell.
            j: Column index of the cell.
        Returns:
            True if the cell contains a ship, otherwise False.
        '''
        return self.cells[i][j] > 0  # Return True if the cell contains a ship (positive value).
