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
            return True
        else:
            print("Row:", input_row, ", Col:", input_col, ", Tile Occupied!")
            return False

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

    def check_game_over(self):

        # cross solution 1
        left_to_right = []
        right_to_left = []
        for i in range(self.board.size):
            left_to_right.append(self.board.marks[i][i])
            right_to_left.append(self.board.marks[i][self.board.size-1-i])
        if all(item == "X" for item in left_to_right) or all(item == "X" for item in right_to_left):
            return "X Won - Cross"
        elif all(item == "O" for item in left_to_right) or all(item == "O" for item in right_to_left):
            return "O Won - Cross"

        # row/column solution
        for i in range(self.board.size):

            # row solution
            if all(item == "X" for item in self.board.marks[i]):
                return "X Won - Row"
            elif all(item == "O" for item in self.board.marks[i]):
                return "O Won - Row"

            # column solution
            columns = []
            for row in self.board.marks:
                columns.append(row[i])
            if all(item == "X" for item in columns):
                return "X Won - Column"
            elif all(item == "O" for item in columns):
                return "O Won - Column"

        # Draw
        free_tile = False
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.marks[i][j] == "E":
                    free_tile = True
        if not free_tile:
            return "Draw"
