import pygame

# All images of the pieces
bpk = pygame.image.load("checker_pieces_drawings/black_king_p.png")
bp = pygame.image.load("checker_pieces_drawings/black_p.png")
rpk = pygame.image.load("checker_pieces_drawings/red_king_p.png")
rp = pygame.image.load("checker_pieces_drawings/red_p.png")


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


# --------------------------------------------------
# Starting positions
# --------------------------------------------------

def create_red_pieces(piece):
    red_piece_set = []

    for row in range(3):
        for col in range(8):

            # Only place pieces on black squares
            if (row + col) % 2 != 0:
                rect = pygame.Rect(
                    col * 46.875,
                    row * 46.875,
                    46.875,
                    46.875
                )

                red_piece_set.append((piece, rect))

    return red_piece_set


def create_black_pieces(piece):
    black_piece_set = []

    for row in range(5, 8):
        for col in range(8):

            # Only place pieces on black squares
            if (row + col) % 2 != 0:
                rect = pygame.Rect(
                    col * 46.875,
                    row * 46.875,
                    46.875,
                    46.875
                )

                black_piece_set.append((piece, rect))

    return black_piece_set