# Filename: renderer.py
# Description: This module defines the Renderer class for the Battleship game, responsible for rendering the game board and handling mouse interactions.
# Inputs: None
# Output: Rendered game window and board
# Other sources for the code: ChatGPT(for proper commenting format).
# Author: Xavier and Andrew
# Creation Date: 9th of September, 2024

from pyray import *  # Importing all the necessary functions from the pyray module, used for rendering.
from .constants import *  # Importing all the constants needed for game logic like cell size, colors, etc.
from .board import Orientation # Importing Orientation enum for ship handling.

class Renderer:
    # Only one renderer, so we make the methods static
    font = None

    @staticmethod
    def draw_font_text(text, posX, posY, fontSize, color):
        '''
        Draw text using the font stored in the static font variable.
        - Usually, this will be set to Roboto.
        - In the case of font failure, fallback to default.
        '''
        if Renderer.font is None: # If the default font is not set
            draw_text(text, posX, posY, fontSize, color) # Use the pyray default font.
            return # Return early since font failed
        
        draw_text_ex(Renderer.font, text, (posX, posY), fontSize, 0, color) # Draw text using custom default font

    @staticmethod
    def get_mouse_board_coordinates():
        '''
        Calculates the board coordinates of the mouse cursor based on its position on the screen.
        - Uses the current mouse position from the pyray library.
        - Adjusts the mouse position relative to the board on the screen.
        Returns: A tuple (i, j) representing the row and column indices of the board.
        '''
        pos = get_mouse_position()  # Get the mouse position from pyray.
        pos.x -= BOARD_PADDING_LEFT  # Adjust the x-coordinate based on the board's position.
        pos.y -= BOARD_PADDING_TOP   # Adjust the y-coordinate based on the board's position.
        i = int(pos.y // CELL_SIZE)  # Convert the y-coordinate into a row index.
        j = int(pos.x // CELL_SIZE)  # Convert the x-coordinate into a column index.

        return (i, j)  # Return the row and column indices as a tuple.

    @staticmethod 
    def draw_row_and_col_numbers(board): 
        for i in range(len(board.cells)): 
            draw_text(str(i+1), BOARD_PADDING - 20, i * CELL_SIZE + CELL_SIZE // 3, 8, BLACK)

        for j in range(len(board.cells[0])): 
            draw_text(str(chr(ASCII_A+j)), BOARD_PADDING + 10 + CELL_SIZE * j, board.rows * CELL_SIZE + 5, 8, BLACK)



    @staticmethod
    def draw_board(board, is_other_player, ship_length = 1, ship_orientation = None):
        '''
        Draws the game board on the screen.
        - The visual appearance of each cell depends on its state (empty, hit, miss, or contains a ship).
        - Cells are rendered differently if the board belongs to the other player (enemy).
        Args:
            board: The Board instance representing the player's or enemy's board.
            is_other_player: Boolean flag indicating if the board being drawn is for the enemy player.
        '''
        # Iterate over each col in the board
        for i in range(board.cols):
            # Draw the column numbers above the columns of the board
            Renderer.draw_font_text(str(i + 1), BOARD_PADDING_LEFT + i * CELL_SIZE + 8, BOARD_PADDING_TOP - 20, 20, BLACK)

        # Iterate over each row and cell in the board
        Renderer.draw_row_and_col_numbers(board)
        for i, row in enumerate(board.cells):

            row_letter = chr(ASCII_A + i).upper() # Get the row letter in uppercase
            Renderer.draw_font_text(row_letter, BOARD_PADDING_LEFT - 20, BOARD_PADDING_TOP + i * CELL_SIZE + 8, 20, BLACK) # Draw the row letter

            for j, cell in enumerate(row):
                # Determine the color of the cell based on its state
                cell_color = WHITE  # Default cell color is BLUE.
                if cell == EMPTY_CELL:  # If the cell is empty, set the color to BLUE.
                    cell_color = WHITE
                elif cell == HIT_CELL:  # If the cell has been hit, set the color to RED.
                    cell_color = RED
                elif cell == MISS_CELL:  # If the attack missed, set the color to GREEN.
                    cell_color = GREEN
                elif cell > 0:  # If the cell contains part of a ship.
                    # Display ship cells based on whether it's an enemy board.
                    if is_other_player:
                        cell_color = WHITE  # For enemy ships, keep the cell color BLUE (hidden).
                    else:
                        cell_color = GRAY  # For the player's ships, display them in GRAY.

                # Draw the border and fill the cell with the determined color
                draw_rectangle_lines(BOARD_PADDING_LEFT + j * CELL_SIZE, BOARD_PADDING_TOP + i * CELL_SIZE, CELL_SIZE, CELL_SIZE, BLACK)  # Draw the cell border.
                draw_rectangle(BOARD_PADDING_LEFT + j * CELL_SIZE + 3, BOARD_PADDING_TOP + i * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6, cell_color)  # Fill the cell with the color.

        # Draw the mouse cursor overlay on the board if it's over a valid cell
        i, j = Renderer.get_mouse_board_coordinates()  # Get the mouse's board coordinates.
        for k in range(ship_length):
            checkX = j + k * (ship_orientation != Orientation.VERTICAL)
            checkY = i + k * (ship_orientation == Orientation.VERTICAL)

            if board.is_valid_cell(checkY, checkX):  # Check if the mouse is over a valid cell.
                # Highlight the cell under the mouse cursor with a semi-transparent yellow overlay.
                draw_rectangle(BOARD_PADDING_LEFT + checkX * CELL_SIZE + 3, BOARD_PADDING_TOP + checkY * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6, Color(255, 255, 0, 100))

    @staticmethod
    def draw_window(game):
        '''
        Initializes and manages the game window.
        - Continuously updates the window to reflect the game state until the window is closed.
        Args:
            game: The Game instance responsible for handling the game's logic and state.
        '''

        # Initialize the window with the specified dimensions and title
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "EECS 581 Project 1 - Battleship")

        # Set the font to Roboto font with 512 px dimensions (for better clarity).
        Renderer.font = load_font_ex("./battleship/resources/roboto.ttf", 512, None, 0)

        while not window_should_close():  # Loop until the user closes the window.
            begin_drawing()  # Start drawing on the window.
            clear_background(WHITE)  # Clear the window with a white background.
            game.game_loop()  # Update the game state and draw the necessary elements.
            end_drawing()  # End drawing and present the frame.
        close_window()  # Close the window when the loop exits.
