import pygame
from pathlib import Path


# --------------------------------------------------
# board.py Variables 
# --------------------------------------------------

RED_COLOR = '#E63022'
BLACK_COLOR = '#000000'
WHITE_COLOR = '#FFFFFF'
TAN_COLOR = "#D2B48C"

BOARD_SIZE = 375
BOARD_ROWS = 8
BOARD_COLS = 8
SQUARE_SIZE = BOARD_SIZE / BOARD_COLS
DISPLAY_INFO = pygame.display.Info()
WIDTH = int(DISPLAY_INFO.current_w * 0.9)
HEIGHT = int(DISPLAY_INFO.current_h * 0.9)
board_x = (WIDTH - BOARD_SIZE) // 2
board_y = (HEIGHT - BOARD_SIZE) // 2

# --------------------------------------------------
# Text
# --------------------------------------------------

font = pygame.font.Font(None, 25)
title_font = pygame.font.Font(None, 72)
ui_font = pygame.font.Font(None, 42)
field_font = pygame.font.Font(None, 36)
status_font = pygame.font.Font(None, 28)

BUILD_VER = "troubleshooters-cg-v0.0.1 - alpha"



BACKGROUND_COLOR ='#222222'

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

ASSETS_DIR = BASE_DIR / "Assets"


def load_asset(filename, size, alpha=True):
    """Loads an image from Assets/ and scales it to size."""
    image = pygame.image.load(ASSETS_DIR / filename)
    image = image.convert_alpha() if alpha else image.convert()
    return pygame.transform.scale(image, size)

## ------------------------------------------------
# Back Button for login, home select_sessions and sesion page
# --------------------------------------------------

back_button = pygame.Rect(40, 40, 130, 52)