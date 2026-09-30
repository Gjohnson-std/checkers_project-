from pathlib import Path

import pygame

from config import RED_COLOR, BLACK_COLOR, TAN_COLOR, WHITE_COLOR
from pieces import (
    red_piece,
    black_piece,
    red_king,
    black_king,
    create_red_pieces,
    create_black_pieces
)


pygame.init()


# --------------------------------------------------
# Window configuration
# --------------------------------------------------

WIDTH = 800
HEIGHT = 600

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Troubleshooters: Checkers Game")


# --------------------------------------------------
# Asset paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

bg_path = BASE_DIR / "Assets" / "bg.jpg"


# --------------------------------------------------
# Background
# --------------------------------------------------

bg = pygame.image.load(bg_path)
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))


# --------------------------------------------------
# Text
# --------------------------------------------------

font = pygame.font.Font(None, 25)

BUILD_VER = "troubleshooters-cg-v0.0.1 - alpha"


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


# --------------------------------------------------
# Create board
# --------------------------------------------------

create_board()


# --------------------------------------------------
# Create pieces
# --------------------------------------------------

red_piece_set = create_red_pieces(red_piece)
black_piece_set = create_black_pieces(black_piece)


# --------------------------------------------------
# Game loop
# --------------------------------------------------

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    # Background
    gameDisplay.blit(bg, (0, 0))


    # Version text
    team_text = font.render(
        BUILD_VER,
        True,
        (0, 0, 0)
    )

    gameDisplay.blit(
        team_text,
        (
            WIDTH - team_text.get_width() - 10,
            HEIGHT - team_text.get_height() - 10
        )
    )


    # Board
    gameDisplay.blit(
        BOARD,
        (213, 113)
    )


    # Pieces
    gameDisplay.blits(red_piece_set)
    gameDisplay.blits(black_piece_set)


    # Update display
    pygame.display.flip()


pygame.quit()