import pygame 
import pandas as pd

pygame.init()

#board here
board = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Checker Pieces")


#All images of the pieces
black_piece_king = pygame.image.load("checker_pieces_drawings/black_king_piece.png")
black_piece = pygame.image.load("checker_pieces_drawings/black_piece.png")
red_piece_king = pygame.image.load("checker_pieces_drawings/red_king_piece.png")
red_piece = pygame.image.load("checker_pieces_drawings/red_piece.png")

#Changing image scale
def image_resize(img):
    return pygame.transform.smoothscale(img, (100, 100))

#use board and create 12 red_pieces and 12 black_pieces
def pieces_starting_pos(red_piece_img, black_piece_image):
    red_piece_arr = [12]
    black_piece_arr = [12]
    

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    board.blit(image_resize(red_piece_king), (0, 0))
    pygame.display.flip()

pygame.quit()


