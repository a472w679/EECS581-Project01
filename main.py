# Filename: main.py
# Description: This script initializes and runs a Battleship game. It creates a game instance and uses the Renderer class to draw the game window.
# Inputs: None
# Output: The rendered game window
# Other sources for the code: ChatGPT (for proper commenting format)
# Authors: Xavier and Andrew
# Creation Date: 9th of September, 2024

from battleship import Game, Renderer  # Importing the Game and Renderer classes from the battleship module.

def main():
    """
    This is the main function that initializes the game.
    - It creates an instance of the Game class.
    - Then, it uses the Renderer class to draw the game window.
    """
    # Create the Game class
    game = Game()  # The game variable is initialized with the Game class instance, which contains the game's logic.

    # Use the Renderer class to draw the game window with the game instance
    Renderer.draw_window(game)  # The Renderer class uses the game instance to draw the game window.

# Check if this script is being run directly
if __name__ == "__main__":
    """
    This condition checks if the script is being executed directly.
    - If true, it calls the main function to start the game.
    """

    main()  # Executes the main function if the script is run directly.
