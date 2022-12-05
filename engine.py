class Player:
    def __init__(self, mark):
        self.mark = mark

    def place_marks(self):
        # get coordinates and place a mark
        # currently ar game class
        # probably unnecessary to move here
        return


class Board:
    def __init__(self, size=5):
        self.size = size
        self.marks = [["E" for row in range(size)] for column in range(size)]
        self.print_board()

    def place_mark(self, input_row, input_col, mark_char="E"):
        if self.marks[input_row][input_col] == "E":
            self.marks[input_row][input_col] = mark_char
            print("Row:", input_row, ", Col:", input_col, ", Mark:", mark_char)
            return 1
        else:
            print("Row:", input_row, ", Col:", input_col, ", Tile Occupied!")
            return 0

    def print_board(self):
        print("Board is ", self.size, "*", self.size, " = ", (self.size * self.size))
        for row in self.marks:
            print(row)


class Game:
    def __init__(self, board_size):
        self.board = Board(board_size)
        self.player1 = Player("X")
        self.player2 = Player("O")
        self.player1_turn = True
        self.over = False

    def make_move(self, input_row, input_col):
        # select current player
        current_player = self.player1 if self.player1_turn else self.player2

        # try to place current player's mark
        if self.board.place_mark(input_row, input_col, current_player.mark):
            self.player1_turn = not self.player1_turn
