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
from enum import Enum

class Powerup(Enum):
    '''Powerup enumeration for powerup types'''
    MULTISHOT  = 0
    BIG_SHOT   = 1

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
        self.ship_count = {} # size of ship is the key, num of cells left of ship is the value 
        self.ship_hits = {} # size of ship is the key, (coordinate is the value) , we use this to store ship locations that have been hit 
        self.num_ship_cells = 0  # Total number of cells occupied by ships, initialized to 0.
        self.board = Board()  # Initializes a new Board instance for the player.
        self.ships_placed = False  # Indicates if ships have been placed, initialized to False.
        self.powerup_options = []  # The set of powerup options the player has on this turn
        self.powerup_choice = None # The index of the above array that the player selects

    def get_ships(self, num):
        """
        Generates ships for the player.
        - num: The number of ships to create.
        - The ships list contains ships from size 1 up to 'num'.
        - Also calculates the total number of ship cells.
        """
        self.ships = [i for i in range(1, num + 1)]  # Create ships with sizes from 1 to 'num'.
        self.num_ship_cells = sum(self.ships)  # Calculate total number of cells that the ships occupy.

        for i in range(1, num+1): 
            self.ship_count[i] = i # sets the ship count for ship to how large it is 
            self.ship_hits[i] = [] # initializes an empty list for ship hits for size i 

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

    def change_cells_to_sunk(self, sunk_ship_size): 
        '''
        Changes the ship cells that now should be sunk to a SUNK_CELL
        - sunk_ship_size: the size of the ship that was sunk
        '''
        # loop over ship_hits dict to make the sunk ship a sunk cell 
        for i, j in self.ship_hits[sunk_ship_size]: 
            self.board.cells[i][j] = SUNK_CELL



    def place_attack(self, i, j):
        '''
        Places an attack on the player's board.
        - i: Row index where the attack occurs.
        - j: Column index where the attack occurs.
        - Returns True if the attack hits a ship, False otherwise. Also returns ship_size if hit 
        '''
        # if this cell has already been interacted with we need to inform the game not to change turns 
        if self.board.cells[i][j] == SUNK_CELL or self.board.cells[i][j] == HIT_CELL or self.board.cells[i][j] == MISS_CELL: 
            return False, MISS_CELL # return False and tell game that the user needs to choose another valid cell 


        if self.board.is_ship(i, j):  # Check if there is a ship at (i, j).
            # Attack hits a ship, mark the cell as a hit.

            # update player ships status 
            ship_size = self.board.cells[i][j]
            self.ship_count[ship_size] -= 1  # decrease the count of the ship that was hit 
            self.num_ship_cells -= 1  # Decrease the count of ship cells after a hit.
            self.ship_hits[ship_size].append((i, j)) 

            # now we can change the board 
            # if the attack sunk a ship we put it as a sunk cell 
            if self.ship_count[ship_size] == 0: 
                self.change_cells_to_sunk(ship_size)
            else: 
                self.board.cells[i][j] = HIT_CELL  # Mark the cell with HIT_CELL constant.

            return True, ship_size  # Attack was a hit.
        else:
            # Attack misses, mark the cell as a miss.
            self.board.cells[i][j] = MISS_CELL  # Mark the cell with MISS_CELL constant.
            return False, EMPTY_CELL  # Attack was a miss and previous cell was an empty cell.

    def get_new_powerup_options(self):
        """
        Randomly get two powerup options. It's a powered up turn.
        """
        self.powerup_options = [Powerup.MULTISHOT, Powerup.BIG_SHOT]

    def is_loss(self):
        """
        Determines if the player has lost the game.
        - A player loses if they have no remaining ship cells (i.e., all ships have been destroyed).
        - Returns True if the player has lost, False otherwise.
        """
        return self.num_ship_cells <= 0  # If no ship cells remain, the player has lost.
