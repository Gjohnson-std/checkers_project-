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
black_king = image_resize(bpk, 50)
red_piece = image_resize(rp, 50)
red_king = image_resize(rpk, 50)


class CheckerPiece(pygame.sprite.Sprite):
    def __init__(self, img, imgk, row, col, SQUARE_AREA, BOARDER_LENGTH, board_x, board_y):
        #checker piece image and rect
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()

        #piece position
        self.row = row
        self.col = col
        self.king = False
        self.imgk = imgk

        self.sa = SQUARE_AREA
        self.bl = BOARDER_LENGTH
        self.bx = board_x
        self.by = board_y
        

        self.update_position()

    def update_position(self):
        self.rect.x = self.col * self.sa + self.bl + self.bx
        self.rect.y = self.row * self.sa + self.bl + self.by

    def move(self, new_row, new_col):
        self.row = new_row
        self.col = new_col
        self.update_position()

    def king_me(self):
        self.king = True
        self.image = self.imgk









