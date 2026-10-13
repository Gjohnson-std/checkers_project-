from pathlib import Path 
from config import RED_COLOR, BLACK_COLOR, TAN_COLOR, WHITE_COLOR
from pieces import  CheckerPiece, CreateCheckerPieceSet
from session_screen import Button
import pygame
import pandas as pd
import customtkinter as tk
import coverage

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

tfont = pygame.font.Font(None, 60)

## Checker Board Configurations 
BOARD_SIZE = 410
BOARD_ROWS = 8
BOARD_COLS = 8 
BOARDER_LENGTH = 5
#adding 5 on every side to account for the boarder
BOARD = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
SQUARE_AREA = (BOARD_SIZE - (BOARDER_LENGTH * 2)) / BOARD_ROWS
#area of every space
board_x, board_y = 200, 100
#middle of board

#CREATING BOARD
def create_board(BOARD, RED_COLOR, BLACK_COLOR):
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                pygame.draw.rect(BOARD, RED_COLOR, (column * SQUARE_AREA + BOARDER_LENGTH, row * SQUARE_AREA + BOARDER_LENGTH, SQUARE_AREA, SQUARE_AREA) )
            else:
                pygame.draw.rect(BOARD, BLACK_COLOR, (column * SQUARE_AREA + BOARDER_LENGTH, row * SQUARE_AREA + BOARDER_LENGTH, SQUARE_AREA, SQUARE_AREA) )
    pygame.draw.rect(BOARD, TAN_COLOR, (0, 0, BOARD_SIZE, BOARD_SIZE), 5)


all_pieces = CreateCheckerPieceSet(SQUARE_AREA, BOARDER_LENGTH, board_x, board_y)
red_piece_set, black_piece_set = all_pieces.create_piecestest()

current_screen = "join"

def go_to_sessions():
    global current_screen
    current_screen = "sessions"

join_button = Button(gameDisplay, 300, 250, 200, 60, "Join Game", go_to_sessions)

available_sessions = ["Session A", "Session B", "Session C"]
session_buttons = []

def join_specific_session(name):
    global current_screen
    print("Joining:", name)
    current_screen = "game"

# Create buttons dynamically
y = 200
for session in available_sessions:
    session_buttons.append(
        Button(gameDisplay, 300, y, 250, 50, session, lambda s=session: join_specific_session(s))
    )
    y += 70


selected_piece = None
# --- GAME LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #for xing out of window
            running = False
        # Button to join a game
        if current_screen == "join":
            join_button.handle_event(event)
        # available games to join
        elif current_screen == "sessions":
            for btn in session_buttons:
                btn.handle_event(event)
        # actual game
        elif current_screen == "game":
            # draw board + pieces
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if selected_piece is None:
                    #if piece not selected 
                    for piece in red_piece_set.sprites() + black_piece_set.sprites():
                        if piece.rect.collidepoint(position):
                            #chooses selected piece if piece is clicked
                            selected_piece = piece
                            break
                else:
                    #if piece is selected, move it
                    mouse_x, mouse_y = position

                    col = int((mouse_x - 200 - BOARDER_LENGTH) // SQUARE_AREA)
                    row = int((mouse_y - 100 - BOARDER_LENGTH) // SQUARE_AREA)
                    #gets the mouse coordinates and the board position

                    selected_piece.move(row, col)
                    #moves piece to the clicked square (doesn't need to be empty but that can be fixed later)
                    selected_piece = None
                    #deselects piece after movement is completed

    
    gameDisplay.blit(bg, (0, 0))

    if current_screen == "join":
        title = tfont.render("[Checkers Title Page]", True, (0,0,0))
        gameDisplay.blit(title, (180, 150))
        join_button.draw()

    elif current_screen == "sessions":
        title = tfont.render("Available Sessions", True, (0,0,0))
        gameDisplay.blit(title, (200, 100))
        for btn in session_buttons:
            btn.draw()

    elif current_screen == "game":
        gameDisplay.blit(bg, (0, 0))
        team_text = font.render(BUILD_VER, True, (0, 0, 0))
        gameDisplay.blit(team_text, (WIDTH - team_text.get_width() - 10, HEIGHT - team_text.get_height() - 10))

        create_board(BOARD, WHITE_COLOR, BLACK_COLOR)
        gameDisplay.blit(BOARD, (200,100))

        red_piece_set.draw(gameDisplay)
        black_piece_set.draw(gameDisplay)
   
    #team_text = font.render(BUILD_VER, True, (0, 0, 0)) # This is how I rendered the font and determined the RGB value
    #gameDisplay.blit(team_text, (WIDTH - team_text.get_width() - 10, HEIGHT - team_text.get_height() - 10))
    #create_board(BOARD, WHITE_COLOR, BLACK_COLOR)
    #gameDisplay.blit(BOARD, (200,100)) # I changed the coordinates to the exact middle here 
    
    #red_piece_set.draw(gameDisplay)
    #black_piece_set.draw(gameDisplay)
    pygame.display.flip()

pygame.quit()
import pygame
import pandas as pd
import customtkinter as tk

pygame.init()

