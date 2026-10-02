from config import RED_COLOR , BLACK_COLOR, TAN_COLOR, WHITE_COLOR
import pygame
from pieces import red_piece, black_piece, bp


pygame.init()
#set up the game window 
Surface = pygame.display.set_mode((600,500), pygame.RESIZABLE)
pygame.display.set_caption("Trouble Shooters: Checkers Game")

## Checker Board Configurations 
BOARD_SIZE = 410
BOARD_ROWS = 8
BOARD_COLS = 8 
BOARDER_LENGTH = 5
#adding 5 on every side to account for the boarder
BOARD = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
SQUARE_AREA = (BOARD_SIZE - (BOARDER_LENGTH * 2)) / BOARD_ROWS
#area of every space


## ---------function to to create the checker board
def create_board(BOARD, RED_COLOR, BLACK_COLOR):
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                pygame.draw.rect(BOARD, RED_COLOR, (column * SQUARE_AREA + BOARDER_LENGTH, row * SQUARE_AREA + BOARDER_LENGTH, SQUARE_AREA, SQUARE_AREA) )
            else:
                pygame.draw.rect(BOARD, BLACK_COLOR, (column * SQUARE_AREA + BOARDER_LENGTH, row * SQUARE_AREA + BOARDER_LENGTH, SQUARE_AREA, SQUARE_AREA) )
    pygame.draw.rect(BOARD, TAN_COLOR, (0, 0, BOARD_SIZE, BOARD_SIZE), 5) 

    
## ---------create the checker board 
create_board(BOARD, WHITE_COLOR, BLACK_COLOR)
Surface.blit(BOARD, (0,0)) 

#function to create pieces at the begining of the game
def create_pieces(red_piece_img, black_piece_img):
    #putting red pieces at start positions
    red_piece_set = []
    for row in range(3):
        #row
        for col in range(8):
            #col
            if(row + col) % 2 != 0:
                bor = 2
                red_piece_set.append((red_piece_img, pygame.Rect(col * SQUARE_AREA + BOARDER_LENGTH, row * SQUARE_AREA + BOARDER_LENGTH, SQUARE_AREA, SQUARE_AREA)))
    #putting black piecees at the starting position
    black_piece_set = []
    for row in range(5, 8):
        #row
        for col in range(8):
            #col
            if(row + col) % 2 != 0:
                black_piece_set.append((black_piece_img, pygame.Rect(col * SQUARE_AREA + BOARDER_LENGTH, row * SQUARE_AREA + BOARDER_LENGTH, SQUARE_AREA, SQUARE_AREA)))
    return red_piece_set, black_piece_set

#createing set of pieces for each player
red_piece_set, black_piece_set = create_pieces(red_piece, black_piece)

Surface.blits(red_piece_set)
Surface.blits(black_piece_set)

pygame.display.flip()
#testing code

#start game 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   

#stop game 
pygame.quit()

#meeting date = 9/29/2026
#minutes = 20
#topics = Finishing sprint 1, creating user stories. merging checker pieces onto release testing main, creating acceptance criteria
