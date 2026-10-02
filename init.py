from pathlib import Path 
from config import RED_COLOR, BLACK_COLOR, TAN_COLOR
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

# Checkers board code starts here
BOARD_SIZE = 375
BOARD_ROWS = 8
BOARD_COLS = 8
BOARD = pygame.Surface((BOARD_SIZE, BOARD_SIZE))

def create_board(BOARD, RED_COLOR, BLACK_COLOR):
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                pygame.draw.rect(BOARD, RED_COLOR, (column * 46.875, row * 46.875, 46.875, 46.875) )
            else:
                pygame.draw.rect(BOARD, BLACK_COLOR, (column * 46.875, row * 46.875, 46.875, 46.875) )
    pygame.draw.rect(BOARD, TAN_COLOR, (0, 0, BOARD_SIZE, BOARD_SIZE), 5) 
    
# --- GAME LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    gameDisplay.blit(bg, (0, 0))
    team_text = font.render(BUILD_VER, True, (0, 0, 0)) # This is how I rendered the font and determined the RGB value
    gameDisplay.blit(team_text, (WIDTH - team_text.get_width() - 10, HEIGHT - team_text.get_height() - 10))
    create_board(BOARD, RED_COLOR, BLACK_COLOR)
    gameDisplay.blit(BOARD, (213,113)) # I changed the coordinates to the exact middle here 
    pygame.display.flip()

pygame.quit()
import pygame
import pandas as pd
import customtkinter as tk

pygame.init()

