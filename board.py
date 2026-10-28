from config import BLACK_COLOR, TAN_COLOR, WHITE_COLOR, WIDTH, HEIGHT, board_x, board_y, BOARD_SIZE, BOARD_ROWS, BOARD_COLS, SQUARE_SIZE
import pygame

# --------------------------------------------------
# Board configuration
# --------------------------------------------------

BOARD_SIZE = 375
BOARD_ROWS = 8
BOARD_COLS = 8
SQUARE_SIZE = BOARD_SIZE / BOARD_COLS

BOARD = pygame.Surface((BOARD_SIZE, BOARD_SIZE))


def create_board():
    """
    Draws the checkerboard onto BOARD.
    """

    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLS):

            if (row + column) % 2 == 0:
                color = WHITE_COLOR
            else:
                color = BLACK_COLOR

            pygame.draw.rect(
                BOARD,
                color,
                (
                    column * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
            )

    pygame.draw.rect(
        BOARD,
        TAN_COLOR,
        (0, 0, BOARD_SIZE, BOARD_SIZE),
        5
    )