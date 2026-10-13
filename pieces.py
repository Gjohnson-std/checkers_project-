import pygame 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "Assets" / "checker_pieces_drawings"
#IMPORTANT!!! - pull from main and commit to release testing main!!!!

#All images of the pieces
bpk = pygame.image.load(IMG_DIR / "black_king_p.png")
bp  = pygame.image.load(IMG_DIR / "black_p.png")
rpk = pygame.image.load(IMG_DIR / "red_king_p.png")
rp  = pygame.image.load(IMG_DIR / "red_p.png")
#Changing image scale
def image_resize(img, resize_val):
    return pygame.transform.smoothscale(img, (resize_val, resize_val))


#resized and ready pieces
#square size = 46.875
black_piece = image_resize(bp, 50)
black_king = image_resize(bpk, 50)
red_piece = image_resize(rp, 50)
red_king = image_resize(rpk, 50)

#creates signular checker piece as a sprite
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
        #for moving piece to new square
        self.row = new_row
        self.col = new_col
        self.update_position()

    def king_me(self):
        #for pieces that reach the opposite end of the board
        self.king = True
        self.image = self.imgk

#creates entire set of checker pieces
class CreateCheckerPieceSet():
    def __init__(self, square_area, border_length, board_x, board_y):
        self.square_area = square_area
        self.border_length = border_length
        self.board_x = board_x
        self.board_y = board_y

    def create_piecestest(self):
        #putting red pieces at start positions
            red_piece_set = pygame.sprite.Group()
            for row in range(3):
                for col in range(8):
                    if(row + col) % 2 != 0:
                        red_piece_set.add(CheckerPiece(red_piece, red_king, row, col, self.square_area, self.border_length, self.board_x, self.board_y))
            #putting black piecees at the starting position
        
            black_piece_set = pygame.sprite.Group()
            for row in range(5, 8):
                for col in range(8):
                    if(row + col) % 2 != 0:
                        black_piece_set.add(CheckerPiece(black_piece, black_king, row, col, self.square_area, self.border_length, self.board_x, self.board_y))
            #produces set of pieces for each player
            return red_piece_set, black_piece_set 









