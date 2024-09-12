# Filename: constants.py
# Description: This module defines the constants used across the Battleship game. These constants include ASCII values for key presses, cell sizes, game colors, and window dimensions.
# Inputs: None
# Output: Provides various constants to be used by other modules in the game.
# Other sources for the code: ChatGPT (for proper commenting format)
# Authors: Xavier and Andrew
# Creation Date: 9th of September, 2024

# ASCII values for specific key presses
ASCII_A = 97  # ASCII value for 'a'. (chr(65) == 'a')
ASCII_0 = 48  # ASCII value for '0'. (chr(48) == '0')
ASCII_B = 66  # ASCII value for 'b'. (chr(98) == 'b')

# Cell and board-related constants
CELL_SIZE = 28  # The size of each cell in the Battleship game board in pixels.

# Game cell status values
HIT_CELL = 0  # Represents a cell that has been hit by an attack.
EMPTY_CELL = -1  # Represents an empty cell on the board.
MISS_CELL = -2  # Represents a cell where an attack was made but no ship was hit.

# Color information for displaying different game states
SHIP_COLOR_INFO = "RIGHT-CLICK = ROTATE\n\nEMPTY = WHITE\nMISSED = GREEN\nHIT = RED"  # Color legend to explain the state of cells on the board.

# Window dimensions
WINDOW_WIDTH = 670  # Width of the game window in pixels.
WINDOW_HEIGHT = 450  # Height of the game window in pixels.

# Padding for board rendering
BOARD_PADDING_LEFT = 200  # Distance in pixels from the left edge of the window to where the board is drawn.
BOARD_PADDING_TOP  = 85   # Distance in pixels from the top edge of the window to where the board is drawn.

# Ship size representation: Any other number than HIT_CELL, EMPTY_CELL, or MISS_CELL corresponds to the size of the ship placed in that cell.
