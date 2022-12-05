from engine import Player
from engine import Board
from engine import Game

# setting up pygame
import pygame

pygame.init()
pygame.font.init()
pygame.display.set_caption("Tic-Tac-Toe Game")

# global variables

SQ_SIZE = 90
H_MARGIN = SQ_SIZE * 0
V_MARGIN = SQ_SIZE * 0

BOARD_SIZE = 5

INDENT = 10

WIDTH = SQ_SIZE * BOARD_SIZE + H_MARGIN
HEIGHT = SQ_SIZE * BOARD_SIZE + V_MARGIN
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# font
font = pygame.font.SysFont("fresansttf", SQ_SIZE)

# colors
GREY = (40, 50, 60)  # for background
WHITE = (150, 150, 150)  # for borders
RED = (250, 50, 100)  # for "X" marks
BLUE = (50, 150, 200)  # for "O" marks
COLORS = {"E": GREY, "X": RED, "O": BLUE}


# grid
def draw_grid(left=0, top=0):
    for row in range(0, BOARD_SIZE):
        for column in range(0, BOARD_SIZE):
            x = left + column * SQ_SIZE
            y = top + row * SQ_SIZE
            square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(SCREEN, WHITE, square, width=3)

            # move half square to right_bottom side
            x += SQ_SIZE // 2
            y += SQ_SIZE // 2

            draw_marks(x, y, row, column)


# marks
def draw_marks(x, y, row, column):
    pygame.draw.circle(SCREEN, COLORS[game.board.marks[row][column]], (x, y), radius=SQ_SIZE // 4)


# create game
game = Game(board_size=BOARD_SIZE)

# pygame loop
animating = True
pausing = False
while animating:

    # track user interaction
    for event in pygame.event.get():

        # user closes the pygame window
        if event.type == pygame.QUIT:
            animating = False

        # user mouse input
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            input_row = y // SQ_SIZE
            input_col = x // SQ_SIZE
            game.make_move(input_row, input_col)

            result = game.check_game_over()
            if result is not None:
                print(result)
                game.over = True

        # user presses key
        if event.type == pygame.KEYDOWN:

            # escape key -- Close the game
            if event.key == pygame.K_ESCAPE:
                animating = False

            # space bar -- Pause the game
            if event.key == pygame.K_SPACE:
                pausing = not pausing

            # Backspace -- Restart the game
            if event.key == pygame.K_r:
                game = Game(board_size=BOARD_SIZE)

    # execution
    if not pausing:
        # draw background
        SCREEN.fill(GREY)

        # draw search grids
        draw_grid()

        # at game over
        if game.over:
            text = game.check_game_over()
            textbox = font.render(text, True, GREY, WHITE)
            t_width, t_height = font.size(text)
            SCREEN.blit(textbox, (BOARD_SIZE * SQ_SIZE // 2 - t_width // 2, BOARD_SIZE * SQ_SIZE // 2 - t_height // 2))

        # update window
        pygame.display.flip()