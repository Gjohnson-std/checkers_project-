from config import (
    RED_COLOR,
    BLACK_COLOR,
    TAN_COLOR,
    BACKGROUND_COLOR
)

import pygame


pygame.init()

BACKGROUND_IMAGE = pygame.image.load("Assets\\bg.jpg")

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500

Surface = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT),
    pygame.RESIZABLE
)

pygame.display.set_caption("Trouble Shooters: Checkers Game")



BOARD_ROWS = 8
BOARD_COLS = 8

BOARD_SIZE = 375



def create_board(board, board_size):
    square_size = board_size / BOARD_ROWS

    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLS):

            if (row + column) % 2 == 0:
                color = RED_COLOR
            else:
                color = BLACK_COLOR

            pygame.draw.rect(
                board,
                color,
                (
                    column * square_size,
                    row * square_size,
                    square_size,
                    square_size
                )
            )

    pygame.draw.rect(
        board,
        TAN_COLOR,
        (0, 0, board_size, board_size),
        5
    )


def draw_game(surface):

    window_width, window_height = surface.get_size()

    background = pygame.transform.scale(
        BACKGROUND_IMAGE,
        (window_width, window_height)
    )

    surface.blit(background, (0,0))

    board_size = min(window_width, window_height)

    board = pygame.Surface((board_size, board_size))

    create_board(board, board_size)

    board_x = (window_width - board_size) // 2
    board_y = (window_height - board_size) // 2

    surface.blit(board, (board_x, board_y))


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            Surface = pygame.display.set_mode(
                (event.w, event.h),
                pygame.RESIZABLE
            )

    draw_game(Surface)

    pygame.display.flip()


pygame.quit()