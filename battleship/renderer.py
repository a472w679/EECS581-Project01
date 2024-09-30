# Filename: renderer.py
# Description: This module defines the Renderer class for the Battleship game, responsible for rendering the game board and handling mouse interactions.
# Inputs: None
# Output: Rendered game window and board
# Other sources for the code: ChatGPT(for proper commenting format).
# Author: Xavier and Andrew
# Creation Date: 9th of September, 2024

from pyray import *  # Importing all the necessary functions from the pyray module, used for rendering.
from .constants import *  # Importing all the constants needed for game logic like cell size, colors, etc.
from .board import Orientation  # Importing Orientation enum for ship handling.
import random  # importing the random module  for ship colors

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
        if Renderer.font is None:  # If the default font is not set
            draw_text(text, posX, posY, fontSize, color)  # Use the pyray default font.
            return  # Return early since font failed

        draw_text_ex(Renderer.font, text, (posX, posY), fontSize, 0, color)  # Draw text using custom default font

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
        pos.y -= BOARD_PADDING_TOP  # Adjust the y-coordinate based on the board's position.
        i = int(pos.y // CELL_SIZE)  # Convert the y-coordinate into a row index.
        j = int(pos.x // CELL_SIZE)  # Convert the x-coordinate into a column index.

        return (i, j)  # Return the row and column indices as a tuple.

    @staticmethod
    def draw_remaining_ships_to_place(player):
        '''
        Draws the  ships the player has left to place in the info margins 
        '''
        cell_ship_size = 20
        draw_text_ex(Renderer.font, f"Player{player.num} Ships", Vector2(10, 130), 20, 1.0, Color(0, 200, 255, 255))
        draw_line(10, 150, 140, 150, BLACK)
        for i, ship in enumerate(player.ships):  # iterate over each ship
            for j in range(ship):  # draw each ship cell corresponding to its size
                ship_color = BLACK
                if ship == player.ships[-1]:  # if current ship that is drawn is the one to be placed by player
                    ship_color = Color(0, 200, 255, 255)  # cyan 

                draw_rectangle_lines(10 + j * (cell_ship_size + 2), 180 + i * 25, cell_ship_size, cell_ship_size,
                                     ship_color)  # draw cell

    @staticmethod
    def draw_ai_buttons(ai_level):
        '''
        Draws the buttons that player can press to select an AI level or PvP mode
        Returns the AI level corresponding to the currently selected button, whether that changed or not
        '''
        button_width = 80
        button_height = 50
        pos = get_mouse_position()  # Get the mouse position from pyray.
        pushed_index = None if ai_level is None else (ai_level + 1)  # Get the index of the button that is pushed
        button_labels = ["PvP", "Easy AI", "Med AI", "Hard AI"]
        new_ai_level = ai_level

        # Looping over the 4 buttons
        for i in range(4):
            x = int(WINDOW_WIDTH / 2 - (2 - i) * (button_width + 10))  # x position of button
            cell = Rectangle(x, 275, button_width, button_height)  # bounding box of button
            draw_rectangle_lines_ex(cell, 3, BLACK)  # draw black outline of button

            # If mouse is hovering over button, shade it light green
            if (pos.x > x and pos.x < x + button_width and pos.y > 275 and pos.y < 275 + button_height):
                draw_rectangle(x + 3, 275 + 3, button_width - 6, button_height - 6, Color(143, 188, 143, 100))

                # If the left button is clicked on this frame, this button has been pushed
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    pushed_index = i
                    new_ai_level = i - 1  # Update the AI level (-1 for PvP, 0-2 for AI levels)

            # If button is selected, shade it gray
            if i == pushed_index:
                draw_rectangle(x + 3, 275 + 3, button_width - 6, button_height - 6, Color(160, 160, 160, 255))

            # Center the text in the button
            text_width = measure_text_ex(Renderer.font, button_labels[i], 18, 0).x
            text_x = x + (button_width - text_width) / 2
            Renderer.draw_font_text(button_labels[i], int(text_x), 290, 18, BLACK)  # Draw the centered button label

        return new_ai_level  # Return the new AI level

    @staticmethod
    def draw_powerup_buttons(pushed_index, label0, label1):
        '''
        Draws the buttons that player can press to select one of their powerups
        Takes the index of the currently selected button and the text to draw in both buttons
        Returns the index of the currently selected button, whether that changed or not
        '''
        if pushed_index != 1:
            pushed_index = 0

        button_width = BOARD_PADDING_LEFT - 10 - 50
        button_height = 50
        pos = get_mouse_position()  # Get the mouse position from pyray.

        x = WINDOW_WIDTH - BOARD_PADDING_LEFT + 10 + 25
        # Looping over the 2 buttons
        for i in range(2):
            y = int(WINDOW_HEIGHT / 2 + (i - 1) *(button_height + 10) + 10/2)  # x position of button
            cell = Rectangle(x, y, button_width, button_height)  # bounding box of button
            draw_rectangle_lines_ex(cell, 3, BLACK)  # draw black outline of button

            # If mouse is hovering over button, shade it light green
            if (pos.x > x and pos.x < x + button_width and pos.y > y and pos.y < y + button_height):
                draw_rectangle(x + 3, y + 3, button_width - 6, button_height - 6, Color(143, 188, 143, 100))

                # If the left button is clicked on this frame, this button has been pushed
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    pushed_index = i

            # If button is selected, shade it gray
            if i == pushed_index:
                draw_rectangle(x + 3, y + 3, button_width - 6, button_height - 6, Color(160, 160, 160, 255))

            label = (label0, label1)[i] # Text to be drawn in the button
            # Center the text in the button
            text_width = measure_text_ex(Renderer.font, label, 18, 0).x
            text_x = x + (button_width - text_width) / 2
            Renderer.draw_font_text(label, int(text_x), y+15, 18, BLACK)  # Draw the centered button label

        return pushed_index  # Return the new AI level

    @staticmethod
    def draw_ship_placement_hover(board, ship_length, ship_orientation):
        # Draw the mouse cursor overlay on the board if it's over a valid cell
        i, j = Renderer.get_mouse_board_coordinates()  # Get the mouse's board coordinates.
        for k in range(ship_length):
            checkX = j + k * (ship_orientation != Orientation.VERTICAL)
            checkY = i + k * (ship_orientation == Orientation.VERTICAL)

            is_ship_placeable = board.is_placeable_on(i, j, ship_length, ship_orientation)
            if not is_ship_placeable and board.is_valid_cell(i,
                                                             j) and ship_length != 1:  # if it is not a placeable ship but mouse is over a valid cell, draw the hover red
                if checkX < board.rows and checkY < board.cols:
                    draw_rectangle(BOARD_PADDING_LEFT + checkX * CELL_SIZE + 3,
                                   BOARD_PADDING_TOP + checkY * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6,
                                   Color(220, 20, 60, 100))
            elif board.is_valid_cell(i, j):  # Check if the mouse is over a valid cell.
                # Highlight the cell under the mouse cursor with a semi-transparent yellow overlay.
                draw_rectangle(BOARD_PADDING_LEFT + checkX * CELL_SIZE + 3, BOARD_PADDING_TOP + checkY * CELL_SIZE + 3,
                               CELL_SIZE - 6, CELL_SIZE - 6, Color(143, 188, 143, 100))

    @staticmethod
    def draw_board(board, is_other_player, ship_length=1, ship_orientation=None):
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
            Renderer.draw_font_text(str(i + 1), BOARD_PADDING_LEFT + i * CELL_SIZE + 8, BOARD_PADDING_TOP - 20, 20,
                                    BLACK)

        # Iterate over each row and cell in the board
        for i, row in enumerate(board.cells):

            row_letter = chr(ASCII_A + i).upper()  # Get the row letter in uppercase
            Renderer.draw_font_text(row_letter, BOARD_PADDING_LEFT - 20, BOARD_PADDING_TOP + i * CELL_SIZE + 8, 20,
                                    BLACK)  # Draw the row letter

            for j, cell in enumerate(row):
                # Determine the color of the cell based on its state
                cell_color = WHITE  # Default cell color is BLUE.
                if cell == EMPTY_CELL:  # If the cell is empty, set the color to BLUE.
                    cell_color = WHITE
                elif cell == SUNK_CELL:
                    cell_color = Color(249, 182, 78, 255)  # yellowish color
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
                # draw_rectangle_lines(BOARD_PADDING_LEFT + j * CELL_SIZE, BOARD_PADDING_TOP + i * CELL_SIZE, CELL_SIZE, CELL_SIZE, BLACK)  # Draw the cell border.
                cell = Rectangle(BOARD_PADDING_LEFT + j * CELL_SIZE, BOARD_PADDING_TOP + i * CELL_SIZE, CELL_SIZE,
                                 CELL_SIZE)
                draw_rectangle_lines_ex(cell, 1.5, BLACK)
                draw_rectangle(BOARD_PADDING_LEFT + j * CELL_SIZE + 3, BOARD_PADDING_TOP + i * CELL_SIZE + 3,
                               CELL_SIZE - 6, CELL_SIZE - 6, cell_color)  # Fill the cell with the color.

        Renderer.draw_ship_placement_hover(board, ship_length, ship_orientation)

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
