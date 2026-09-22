from config import RED_COLOR , BLACK_COLOR, TAN_COLOR
import pygame


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
def create_board(BOARD, RED_COLOR, BLACK_COLOR):
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                pygame.draw.rect(BOARD, RED_COLOR, (column * 46.875, row * 46.875, 46.875, 46.875) )
            else:
                pygame.draw.rect(BOARD, BLACK_COLOR, (column * 46.875, row * 46.875, 46.875, 46.875) )
    pygame.draw.rect(BOARD, TAN_COLOR, (0, 0, BOARD_SIZE, BOARD_SIZE), 5) 
    
## ---------create the checker board 
create_board(BOARD, RED_COLOR, BLACK_COLOR)
Surface.blit(BOARD, (0,0)) 
pygame.display.flip()

#start game 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   

#stop game 
pygame.quit()
