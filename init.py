from pathlib import Path 
from config import RED_COLOR, BLACK_COLOR, TAN_COLOR, WHITE_COLOR
from pieces import red_piece, black_piece
import pygame
import pandas as pd
import customtkinter as tk

pygame.init()

# Base directory finds the path for the parent folder where file is stored 
BASE_DIR = Path(__file__).resolve().parent

# Updated path using pathlib to pull the assets dynamically 
bg_path = BASE_DIR / "Assets" / "bg.jpg"

WIDTH, HEIGHT = 800, 600  # Change these numbers to match your desired window size
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Troubleshooters: Checkers Game")

bg = pygame.image.load(bg_path)
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

font = pygame.font.Font(None, 25) # Placeholder font can be changed later to a system font 
BUILD_VER = "troubleshooters-cg-v0.0.1 - alpha"

## Checker Board Configurations 
BOARD_SIZE = 410
BOARD_ROWS = 8
BOARD_COLS = 8 
BOARDER_LENGTH = 5
#adding 5 on every side to account for the boarder
BOARD = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
SQUARE_AREA = (BOARD_SIZE - (BOARDER_LENGTH * 2)) / BOARD_ROWS
#area of every space

def create_board(BOARD, RED_COLOR, BLACK_COLOR):
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                pygame.draw.rect(BOARD, RED_COLOR, (column * SQUARE_AREA + BOARDER_LENGTH, row * SQUARE_AREA + BOARDER_LENGTH, SQUARE_AREA, SQUARE_AREA) )
            else:
                pygame.draw.rect(BOARD, BLACK_COLOR, (column * SQUARE_AREA + BOARDER_LENGTH, row * SQUARE_AREA + BOARDER_LENGTH, SQUARE_AREA, SQUARE_AREA) )
    pygame.draw.rect(BOARD, TAN_COLOR, (0, 0, BOARD_SIZE, BOARD_SIZE), 5)

def create_pieces(red_piece_img, black_piece_img, board_x, board_y):
    #putting red pieces at start positions
    red_piece_set = []
    for row in range(3):
        #row
        for col in range(8):
            #col
            if(row + col) % 2 != 0:
                bor = 2
                red_piece_set.append((red_piece_img, pygame.Rect(col * SQUARE_AREA + BOARDER_LENGTH + board_x, row * SQUARE_AREA + BOARDER_LENGTH + board_y, SQUARE_AREA, SQUARE_AREA)))
    #putting black piecees at the starting position
    black_piece_set = []
    for row in range(5, 8):
        #row
        for col in range(8):
            #col
            if(row + col) % 2 != 0:
                black_piece_set.append((black_piece_img, pygame.Rect(col * SQUARE_AREA + BOARDER_LENGTH + board_x, row * SQUARE_AREA + BOARDER_LENGTH + board_y, SQUARE_AREA, SQUARE_AREA)))
    return red_piece_set, black_piece_set

#createing set of pieces for each player

# --- GAME LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    gameDisplay.blit(bg, (0, 0))
    team_text = font.render(BUILD_VER, True, (0, 0, 0)) # This is how I rendered the font and determined the RGB value
    gameDisplay.blit(team_text, (WIDTH - team_text.get_width() - 10, HEIGHT - team_text.get_height() - 10))
    create_board(BOARD, WHITE_COLOR, BLACK_COLOR)
    gameDisplay.blit(BOARD, (200,100)) # I changed the coordinates to the exact middle here 
    red_piece_set, black_piece_set = create_pieces(red_piece, black_piece, 200, 100)
    gameDisplay.blits(red_piece_set)
    gameDisplay.blits(black_piece_set)
    pygame.display.flip()

pygame.quit()
import pygame
import pandas as pd
import customtkinter as tk

pygame.init()

