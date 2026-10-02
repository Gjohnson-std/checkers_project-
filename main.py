from config import RED_COLOR , BLACK_COLOR, TAN_COLOR, WHITE_COLOR
import pygame
from pieces import red_piece, black_piece, red_piece_start


pygame.init()
#set up the game window 
Surface = pygame.display.set_mode((600,500), pygame.RESIZABLE)
pygame.display.set_caption("Trouble Shooters: Checkers Game")

## Checker Board Configurations 
BOARD_SIZE = 375
BOARD_ROWS = 8
BOARD_COLS = 8 
BOARD = pygame.Surface((BOARD_SIZE, BOARD_SIZE))


## ---------function to to create the checker board
def create_board(BOARD, WHITE_COLOR, BLACK_COLOR):
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                pygame.draw.rect(BOARD, WHITE_COLOR, (column * 46.875, row * 46.875, 46.875, 46.875) )
            else:
                pygame.draw.rect(BOARD, BLACK_COLOR, (column * 46.875, row * 46.875, 46.875, 46.875) )
    #pygame.draw.rect(BOARD, TAN_COLOR, (0, 0, BOARD_SIZE, BOARD_SIZE), 5) 

    
## ---------create the checker board 
create_board(BOARD, WHITE_COLOR, BLACK_COLOR)
Surface.blit(BOARD, (0,0)) 

red_piece_set = []
for row in range(3):
    #row
    for col in range(8):
        #col
        if(row + col) % 2 != 0:
            bor = 2
            red_piece_set.append((red_piece, pygame.Rect(col * 46.875, row * 46.875, 46.875, 46.875)))
#creating each piece at the starting position

black_piece_set = []
for row in range(5, 8):
    #row
    for col in range(8):
        #col
        if(row + col) % 2 != 0:
            black_piece_set.append((black_piece, pygame.Rect(col * 46.875, row * 46.875, 46.875, 46.875)))


#testing pieces
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
