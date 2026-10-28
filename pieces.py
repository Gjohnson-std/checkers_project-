import pygame

# All images of the pieces
bpk = pygame.image.load("checker_pieces_drawings/black_king_p.png")
bp = pygame.image.load("checker_pieces_drawings/black_p.png")
rpk = pygame.image.load("checker_pieces_drawings/red_king_p.png")
rp = pygame.image.load("checker_pieces_drawings/red_p.png")

#changing inage scale
# --------------------------------------------------
# Image resizing
# --------------------------------------------------

def image_resize(img, resize_val):
    return pygame.transform.smoothscale(
        img,
        (resize_val, resize_val)
    )

# --------------------------------------------------
# Resized pieces
# --------------------------------------------------

black_piece = image_resize(bp, 45.875)
red_piece = image_resize(rp, 46.875)

black_king = image_resize(bpk, 45.875)
red_king = image_resize(rpk, 46.875)


#defining sprite class to give pieces mobility
class CheckerPiece(pygame.sprite.Sprite):
    def __init__(self, pieceID, piece_img, king_piece_img, board_x, board_y, row, col, square_size):
        super().__init__()
        """Creates Pieces"""
        self.image = piece_img
        self.rect = self.image.get_rect(topleft=(board_x + square_size * col, board_y + square_size * row))

        self.pieceID = pieceID
        self.piece_img = piece_img
        self.king_piece_img = king_piece_img
        self.board_x = board_x
        self.board_y = board_y
        #board_x and board_y is the top left corner position of the board
        self.square_size = square_size
        self.row = row
        self.col = col
        
        self.king = False

    def king_me(self):
        """King me for when a piece reaches the opposite side of the board"""
        self.king = True
        self.image = self.king_piece_img
        self.rect = self.image.get_rect(topleft=(self.board_x + self.square_size * self.col, self.board_y + self.square_size * self.row))

    def update_pos(self):
        """Updates the position of the piece after it has been told to move"""
        self.rect.x = self.board_x + (self.col * self.square_size)
        self.rect.y = self.board_y + (self.row * self.square_size)

    def move(self, new_row, new_col):
        """Moves a piece to a new column and row."""
        self.row = new_row
        self.col = new_col
        self.update_pos()

    def set_pieceID(self, piece_number, piece_type):
        """Sets the Piece Name so that it can be logged and identified"""
        self.pieceID = piece_type + " " + str(piece_number)


# --------------------------------------------------
# Starting positions
# --------------------------------------------------

def create_red_pieces(board_x, board_y):
    red_pieces = pygame.sprite.Group()
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 != 0:
                red_pieces.add(CheckerPiece("", red_piece, red_king, board_x, board_y, row, col, 46.875))
                #create each red piece at starting position
    for index, piece in enumerate(red_pieces):
        piece.set_pieceID(index, "Red")
        #name each red piece
    return red_pieces


def create_black_pieces(board_x, board_y):
    black_pieces = pygame.sprite.Group()
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 != 0:
                black_pieces.add(CheckerPiece("", black_piece, black_king, board_x, board_y, row, col, 46.875))
                #creating black pieces in starting positions
    for index, piece in enumerate(black_pieces):
        piece.set_pieceID(index, "Black")
        #name each black piece
    return black_pieces 