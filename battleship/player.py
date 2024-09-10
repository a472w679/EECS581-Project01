from .board import Board
from .constants import * 

class Player: 
    def __init__(self, num): 
        self.num = num
        self.ships = []
        self.num_ship_cells = 0
        self.board = Board()
        self.ships_placed = False 

    def get_ships(self, num): 
        self.ships = [i for i in range(1, num+1)]
        self.num_ship_cells = sum(self.ships)


    # attempts to place a ship if success, return true, else return false 
    def place_ship(self, i, j, ship_size): 
        if self.board.is_placeable_on(i, j, ship_size): 
            for pos in range(ship_size): 
                self.board.cells[i][j + pos] = ship_size

            return True 
        return False 

    def place_attack(self, i, j): 
        '''
        used to place attack from enemy player 
        return true if player hit and false if miss
        '''
        if self.board.is_ship(i, j): 
            self.board.cells[i][j] = HIT_CELL 
            self.num_ship_cells -= 1 
            return True 
        else: 
            self.board.cells[i][j] = MISS_CELL
            return False 


    def is_loss(self): 
        return self.num_ship_cells <= 0 