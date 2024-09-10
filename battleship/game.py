from pyray import * 
from .renderer import Renderer
from .player import Player 
from .constants import * 

class Game: 
    def __init__(self): 
        # game info 
        self.turn = 1  # "player 1 or 2's turn" 
        self.player1 = Player(1)   
        self.player2 = Player(2)   
        self.show_own_board = False  # whether the player wants to look at their own board 

        # utility lookup tables 
        self.player_lookup_table = {1: self.player1, 2: self.player2} # turn 1 corresponds to player 1 
        self.enemy_lookup_table = {1: self.player2, 2: self.player1} # player 1's enemy is player 2


        # game phases 
        self.menu_phase = True 
        self.place_ship_phase = False  
        self.attack_phase = False 

        # game messages 
        self.message = "Enter Ship Number to play with (Min: 0, Max: 5)"
        self.last_move_message = "" # What the last move's result was 
        self.secondary_message = ""
        self.color_info = SHIP_COLOR_INFO

    def get_placement(self, player): 
        '''
        placing ships 
        '''

        i, j = Renderer.get_mouse_board_coordinates()

        if (is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT)): 
            res = player.place_ship(i, j, player.ships[-1])
            if not res: 
                self.last_move_message = "not a correct placement!"
            else: 
                player.ships.pop()

        # check if player finished placing ships 
        if not player.ships: 
            player.ships_placed = True 

    def get_attack(self, player, enemy): 
        '''
        attacking other the enemy's board
        '''

        i, j = Renderer.get_mouse_board_coordinates()
        if (is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT)): 
            if (enemy.board.is_valid_cell(i, j)): 
                res = enemy.place_attack(i, j)
                if res: 
                    self.last_move_message = f"Player {player.num} has hit a ship!"
                else: 
                    self.last_move_message = f"Player {player.num} has missed!"

                return True 
        
        return False 

    def show_menu(self): 
        key = get_key_pressed() - ASCII_0
        if key > 0 and key <= 5: 
            self.player1.get_ships(key)
            self.player2.get_ships(key)
            self.message = "It is Player 1's turn to place their ships "
            self.menu_phase = False 
            self.place_ship_phase = True 


    def show_place_ship_phase(self): 
        Renderer.draw_board(self.player_lookup_table[self.turn].board, False)
        self.get_placement(self.player_lookup_table[self.turn])
        if self.player1.ships_placed: 
            self.message = "It is Player 2's turn to place their ships"
            self.turn = 2 
        else: 
            self.turn = 1

        if self.player1.ships_placed and self.player2.ships_placed: 
            self.place_ship_phase = False 
            self.attack_phase = True
            self.secondary_message = "Press (B) to show own board"

    def toggle_show_board(self): 
        key = get_key_pressed()
        if key == ASCII_B: 
            if self.show_own_board: 
                self.secondary_message = "Press (B) to show own board"
                self.show_own_board = False 
            else: 
                self.secondary_message = "Viewing Own Board\n[Press B to view enemy]"
                self.show_own_board = True 

    def show_attack_phase(self): 
        self.toggle_show_board()
        self.message = f"It is Player {self.turn}'s turn to attack"

        current_player = self.player_lookup_table[self.turn]
        current_enemy_player = self.enemy_lookup_table[self.turn]
        if self.show_own_board: 
            Renderer.draw_board(current_player.board, False)
            if (is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT)): 
                self.last_move_message = "Can't attack! Currently viewing own board!"
        else: 
            Renderer.draw_board(current_enemy_player.board, True)

            res = self.get_attack(current_player, current_enemy_player) 
            if current_enemy_player.is_loss(): 
                self.message = f"Player {self.turn} has won!" 
                self.attack_phase = False 

            if res and self.turn == 1: 
                self.turn = 2
            elif res and self.turn == 2:
                self.turn = 1  


    def draw_info_messages(self): 
        '''
        draw info text below board
        '''

        draw_text(self.message, 150, 300, 20, BLACK)
        draw_text(self.last_move_message, 150, 320, 20, RED)
        draw_text(self.secondary_message, 150, 340, 20, GREEN)
        draw_text(self.color_info, 10, 10, 10, BLACK)


    def game_loop(self):
        '''
        The main game loop 
        '''
        self.draw_info_messages()
        if self.menu_phase:
            self.show_menu()
        elif self.place_ship_phase: 
            self.show_place_ship_phase()
        elif self.attack_phase: 
            self.show_attack_phase()