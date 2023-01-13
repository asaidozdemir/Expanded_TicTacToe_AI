import random
import sys

MAX_DEPTH = 6
X_VAL = 264
O_VAL = 237
E_VAL = 96


class Player:
    def __init__(self, mark):
        self.mark = mark


class Board:
    def __init__(self, size=5):
        self.size = size
        self.marks = [["E" for row in range(size)] for column in range(size)]
        self.available_moves = size * size

    def place_mark(self, input_row, input_col, mark_char="E"):
        if self.marks[input_row][input_col] == "E":
            self.marks[input_row][input_col] = mark_char
            self.available_moves -= 1
            print("Row:", input_row, ", Col:", input_col, ", Marking:", mark_char)
            return True
        else:
            print("Row:", input_row, ", Col:", input_col, ", Tile Occupied!")
            return False

    def set_mark_at(self, row, col, mark_char):
        self.marks[row][col] = mark_char

    def print_board(self):
        print("Board is ", self.size, "*", self.size, " = ", (self.size * self.size))
        for row in self.marks:
            print(row)

    def is_tile_marked(self, row, col):
        return self.marks[row][col] != "E"

    def get_mark_value_at(self, row, col):
        if self.marks[row][col] == "X":
            return X_VAL
        elif self.marks[row][col] == "O":
            return O_VAL
        elif self.marks[row][col] == "E":
            return E_VAL

    def any_moves_available(self):
        return self.available_moves > 0

    def is_mark_at_cross_lines(self, row, col):
        is_at_cross = False

        for i in range(self.size):
            if i == row and i == col:
                is_at_cross = True
                break

        index_max = self.size - 1
        for i in range(index_max + 1):
            if i == row and index_max - i == col:
                is_at_cross = True
                break

        return is_at_cross


class Game:
    def __init__(self, board_size):
        self.board = Board(board_size)
        self.playerHuman = Player("O")
        self.playerAI = Player("X")
        self.playerHuman_turn = False
        self.over = False

    def make_move(self, input_row, input_col):

        # select current player
        current_player = self.playerHuman if self.playerHuman_turn else self.playerAI

        # try to place current player's mark
        if self.board.place_mark(input_row, input_col, current_player.mark):
            self.playerHuman_turn = not self.playerHuman_turn

    def check_game_over(self):

        # cross solution 1
        left_to_right = []
        right_to_left = []
        for i in range(self.board.size):
            left_to_right.append(self.board.marks[i][i])
            right_to_left.append(self.board.marks[i][self.board.size - 1 - i])
        if all(item == "X" for item in left_to_right) or all(item == "X" for item in right_to_left):
            return "Red Won - Cross"
        elif all(item == "O" for item in left_to_right) or all(item == "O" for item in right_to_left):
            return "Blue Won - Cross"

        # row/column solution
        for i in range(self.board.size):

            # row solution
            if all(item == "X" for item in self.board.marks[i]):
                return "Red Won - Row"
            elif all(item == "O" for item in self.board.marks[i]):
                return "Blue Won - Row"

            # column solution
            columns = []
            for row in self.board.marks:
                columns.append(row[i])
            if all(item == "X" for item in columns):
                return "Red Won - Column"
            elif all(item == "O" for item in columns):
                return "Blue Won - Column"

        # Draw or X Rule
        free_tile = False
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.marks[i][j] == "E":
                    free_tile = True

        if not free_tile:
            x_rule = []
            x_count = 0
            o_count = 0

            # assemble all marks on cross lines
            for i in range(self.board.size):
                x_rule.append(self.board.marks[i][i])
                x_rule.append(self.board.marks[i][self.board.size - 1 - i])

            # if size is odd remove center-piece
            if self.board.size % 2:
                x_rule.remove(self.board.marks[self.board.size // 2][self.board.size // 2])

            for item in x_rule:
                if item == "X":
                    x_count += 1
                elif item == "O":
                    o_count += 1

            if x_count > o_count:
                return "Red Won - X Rule"
            elif x_count < o_count:
                return "Blue Won - X Rule"
            elif x_count == o_count:
                return "Draw"


class Minimax:
    def __init__(self):
        print()

    def get_best_move(self, board):
        best_move = [-1, -1]
        best_value = -sys.maxsize

        # Select place on cross lines first
        for row in range(board.size):
            for col in range(board.size):
                if not board.is_tile_marked(row, col) and board.is_mark_at_cross_lines(row, col):
                    board.set_mark_at(row, col, "X")
                    move_value = self.minimax(board, MAX_DEPTH, -sys.maxsize, sys.maxsize, False)
                    board.set_mark_at(row, col, "E")
                    if move_value > best_value:
                        best_move[0] = row
                        best_move[1] = col
                        best_value = move_value

        # Select place on whole table if not selected on cross lines before
        if best_value != -sys.maxsize:
            for row in range(board.size):
                for col in range(board.size):
                    if not board.is_tile_marked(row, col):
                        board.set_mark_at(row, col, "X")
                        move_value = self.minimax(board, MAX_DEPTH, -sys.maxsize, sys.maxsize, False)
                        board.set_mark_at(row, col, "E")
                        if move_value > best_value:
                            best_move[0] = row
                            best_move[1] = col
                            best_value = move_value

        # Select place on cross lines randomly if no suitable place found before
        randomly_cross_move_selected = False
        if best_value == -sys.maxsize:
            possible_moves=[]
            for row in range(board.size):
                for col in range(board.size):
                    if not board.is_tile_marked(row, col) and board.is_mark_at_cross_lines(row, col):
                        possible_moves.append([row,col])
            if len(possible_moves) !=0:
                pos = random.randint(0, len(possible_moves)-1)
                best_move[0]=possible_moves[pos][0]
                best_move[1]=possible_moves[pos][1]
                randomly_cross_move_selected = True

        # Select place on whole table randomly if no suitable place found before
        if not randomly_cross_move_selected:
            if best_value == -sys.maxsize:
                possible_moves=[]
                for row in range(board.size):
                    for col in range(board.size):
                        if not board.is_tile_marked(row, col):
                            possible_moves.append([row,col])
                if len(possible_moves) != 0:
                    pos = random.randint(0, len(possible_moves)-1)
                    best_move[0] = possible_moves[pos][0]
                    best_move[1] = possible_moves[pos][1]
                    randomly_cross_move_selected = True

        return best_move

    def minimax(self, board, depth, alpha, beta, is_max):
        board_val = self.evaluate_board(board, depth)
        if abs(board_val) > 0 or depth == 0 or not board.any_moves_available():
            return board_val

        if is_max:
            highest_val = -sys.maxsize
            for row in range(board.size):
                for col in range(board.size):
                    if not board.is_tile_marked(row, col):
                        board.set_mark_at(row, col, "X")
                        highest_val = max(highest_val, self.minimax(board, depth - 1, alpha, beta, False))
                        board.set_mark_at(row, col, "E")
                        alpha = max(alpha, highest_val)
                        if alpha >= beta:
                            return highest_val
            return highest_val

        else:
            lowest_val = sys.maxsize
            for row in range(board.size):
                for col in range(board.size):
                    if not board.is_tile_marked(row, col):
                        board.set_mark_at(row, col, "O")
                        lowest_val = min(lowest_val, self.minimax(board, depth - 1, alpha, beta, True))
                        board.set_mark_at(row, col, "E")
                        beta = min(beta, lowest_val)
                        if beta <= alpha:
                            return lowest_val
            return lowest_val

    def evaluate_board(self, board, depth):
        x_win = X_VAL * board.size
        o_win = O_VAL * board.size

        # Row
        row_sum = 0
        for row in range(board.size):
            for col in range(board.size):
                row_sum += board.get_mark_value_at(row, col)
            if row_sum == x_win:
                return 10 + depth
            elif row_sum == o_win:
                return -10 - depth
            row_sum = 0

        # Column
        row_sum = 0
        for col in range(board.size):
            for row in range(board.size):
                row_sum += board.get_mark_value_at(row, col)
            if row_sum == x_win:
                return 10 + depth
            elif row_sum == o_win:
                return -10 - depth
            row_sum = 0

        # Cross 1
        row_sum = 0
        for i in range(board.size):
            row_sum += board.get_mark_value_at(i, i)
        if row_sum == x_win:
            return 10 + depth
        elif row_sum == o_win:
            return -10 - depth

        # Cross 2
        row_sum = 0
        index_max = board.size - 1
        for i in range(index_max + 1):
            row_sum += board.get_mark_value_at(i, index_max - i)
        if row_sum == x_win:
            return 10 + depth
        elif row_sum == o_win:
            return -10 - depth

        return 0
