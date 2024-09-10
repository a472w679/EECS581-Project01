class Board: 
    def __init__(self, rows=10, cols=10): 
        self.rows = rows
        self.cols = cols
        self.cells = [[-1] * rows for _ in range(cols)] 

    def is_valid_cell(self, i, j): 
        # bounds check
        return i >= 0 and i < self.rows and j >= 0 and j < self.cols 

    def is_placeable_on(self, i, j, ship_size): 
        # check if ships already exist here 
        # return false if can't place a ship 
        # true if you can 
        if self.is_valid_cell(i, j) and (ship_size + j - 1) < self.cols: 
            for x in range(ship_size):
                if self.cells[i][j+x] != -1:  
                    return False 
        else: 
            return False 

        return True 


    def is_ship(self, i, j): 
        # cell has a ship if it is a number greater than 0 
        return self.cells[i][j] > 0 

