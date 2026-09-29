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
black_piece = image_resize(bp, 45.875)
red_piece = image_resize(rp, 46.875)

#gets pieces in starting position and returns a list that will be using in main method in Surface.blits(list)
def red_piece_start(red_piece):
    red_piece_set = []
    for row in range(3):
        #row
        for col in range(8):
            #col
            if(row + col) % 2 != 0:
                bor = 2
                red_piece_set.append((red_piece, pygame.Rect(col * 46.875, row * 46.875, 46.875, 46.875)))
    return red_piece_set
    #creating each piece at the starting position

if __name__ == "__main__":
    red_piece_start(red_piece)





