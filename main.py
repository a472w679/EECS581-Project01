ASCII_A = 97 # chr(65) == "A"

class Board: 
    def __init__(self, rows=10, cols=10): 
        self.rows = rows
        self.cols = cols
        self.cells = [[-1] * rows for _ in range(cols)] 
        # 0 = hit 
        # -1 = empty cell 
        # any other number = ship size 

    def is_placeable_on(self, i, j, ship_size): 
        # check if ships already exist here 
        for x in range(ship_size): 
            if self.cells[i][j+x] != -1:  
                return False 

        # check bounds 
        return self.is_valid_cell(i, j) and (ship_size + j) < self.rows 

    def is_valid_cell(self, i, j): 
        return i < self.rows and j < self.cols 

    def is_ship(self, i, j): 
        if self.is_valid_cell(i, j): 
            return self.cells[i][j] > 0 


class Renderer: 
    @staticmethod
    def print_board(board): 
        '''
        for visual debugging purposes 
        '''
        cols = [chr(ASCII_A+i) for i in range(len(board.cells))]
        print(cols)


        for i, row in enumerate(board.cells): 
            print(i, end=" ")
            print(row, end = "\n") 

    @staticmethod 
    def draw_other_player(self): 
        pass 


class Player: 
    def __init__(self, num): 
        self.num = num
        self.ships = [2]
        self.num_ship_cells = sum(self.ships)
        self.board = Board()
        self.won = False 

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
        '''
        if self.board.is_ship(i, j): 
            self.board.cells[i][j] = 0 
            self.num_ship_cells -= 1 
            return True 

        return False 

    def is_loss(self): 
        return self.num_ship_cells <= 0 







class Game: 
    def __init__(self, num_ships=5): 
        self.turn = 1  # "player 1 or 2" 
        self.player1 = Player(1)   
        self.player2 = Player(2)   
        self.num_ships = num_ships

    def get_placement(self, player): 
        getting_placement = True 
        while getting_placement: 
            Renderer.print_board(player.board)
            row = int(input("what row would you like to place: "))
            col = ord(input("what col would you like to place: ")) - ASCII_A

            ship_size = int(input(f"what ship size would you like to place: {player.ships} "))

            res = player.place_ship(row, col, ship_size)
            if res: 
                player.ships.remove(ship_size)
            else: 
                print("not a correct placement!")
                continue 

            if not player.ships: 
                getting_placement = False 
                print("finished placing ships")

    def get_attack(self, player, enemy): 
        Renderer.print_board(enemy.board)
        row = int(input("what row would you like to attack: "))
        col = ord(input("what col would you like to attack: ")) - ASCII_A

        res = enemy.place_attack(row, col)
        if res: 
            print("ship hit!") 
        else: 
            print("ship missed")



    def loop(self):
        game_running = True 
        place_ship_phase = True 
        attack_phase = False 
        while game_running: 
            if place_ship_phase: 
                print(f"player 1 Place your ships")
                self.get_placement(self.player1)

                print(f"player2 place your ships") 
                self.get_placement(self.player2)
                attack_phase = True
                place_ship_phase = False 
            elif attack_phase: 
                if self.turn == 1: 
                    print("It is player 1's turn")
                    self.get_attack(self.player1, self.player2)
                    if self.player2.is_loss(): 
                        print("player 1 has won!") 
                        game_running = False

                    self.turn = 2 
                elif self.turn == 2: 
                    print("It is player 2's turn")
                    self.get_attack(self.player2, self.player1)
                    if self.player1.is_loss(): 
                        print("player 2 has won!") 
                        game_running = False

                    self.turn = 1 




def main(): 
    g = Game()
    g.loop()

if __name__ == "__main__": 
    main()


