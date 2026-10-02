import pygame 

#All images of the pieces
bpk = pygame.image.load("checker_pieces_drawings/black_king_p.png")
bp = pygame.image.load("checker_pieces_drawings/black_p.png")
rpk = pygame.image.load("checker_pieces_drawings/red_king_p.png")
rp = pygame.image.load("checker_pieces_drawings/red_p.png")

#Changing image scale
def image_resize(img, resize_val):
    return pygame.transform.smoothscale(img, (resize_val, resize_val))


#resized and ready pieces
#square size = 46.875
black_piece = image_resize(bp, 50)
red_piece = image_resize(rp, 50)







