from pyray import * 
from .constants import * 


class Renderer: 
    # Only one renderer, so we make the methods static  
    @staticmethod 
    def get_mouse_board_coordinates(): 
        pos = get_mouse_position()
        pos.x -= BOARD_PADDING # normalizing position to board position on screen
        i = int(pos.y // CELL_SIZE)
        j = int(pos.x // CELL_SIZE)


        return (i, j)
    
    @staticmethod
    def draw_board(board, is_other_player): 
        # is_other_player means that the board we are drawing is the enemy
        # the player shouldn't be able to see their ships 
        for i, row in enumerate(board.cells):
            for j, cell in enumerate(row): 
                cell_color = BLUE
                if cell == EMPTY_CELL: 
                    cell_color = BLUE 
                elif cell == HIT_CELL: 
                    cell_color = RED
                elif cell == MISS_CELL: 
                    cell_color = GREEN
                elif cell > 0: 
                    if is_other_player: 
                        cell_color = BLUE 
                    else: 
                        cell_color = GRAY 

                draw_rectangle_lines(BOARD_PADDING + j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE, BLACK) 
                draw_rectangle(BOARD_PADDING + j * CELL_SIZE + 3, i * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6, cell_color) 


        # drawing mouse position on board 
        i, j = Renderer.get_mouse_board_coordinates()
        if board.is_valid_cell(i, j): 
            # draw yellow overlay on board if mouse hover 
            draw_rectangle(BOARD_PADDING + j * CELL_SIZE + 3, i * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6, Color(255, 255, 0, 100))  



    @staticmethod
    def draw_window(game): 
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "EECS 581 Project 1 - Battleship")
        while not window_should_close():
            begin_drawing()
            clear_background(WHITE)
            game.game_loop()
            end_drawing()
        close_window()