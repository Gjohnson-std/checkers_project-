from config import (
    BOARD_SIZE,
    BOARD_ROWS,
    BOARD_COLS,
    SQUARE_SIZE,
    board_x,
    board_y, 
    WHITE_COLOR,
    BLACK_COLOR,
    TAN_COLOR,
) 
import pygame
import pandas as pd

# --------------------------------------------------
# Board configuration
# --------------------------------------------------
BOARD = pygame.Surface((BOARD_SIZE, BOARD_SIZE))

#this function creates the checkerboard 
def create_board():
    """
    Draws the checkerboard onto BOARD.
    """

    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLS):

            if (row + column) % 2 == 0:
                color = WHITE_COLOR
            else:
                color = BLACK_COLOR

            pygame.draw.rect(
                BOARD,
                color,
                (
                    column * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
            )

    pygame.draw.rect(
        BOARD,
        TAN_COLOR,
        (0, 0, BOARD_SIZE, BOARD_SIZE),
        5
    )

# --------------------------------------------------
# Checker Pieces Positioning 
# --------------------------------------------------
 
# All images of the pieces
bpk = pygame.image.load("checker_pieces_drawings/black_king_p.png")
bp = pygame.image.load("checker_pieces_drawings/black_p.png")
rpk = pygame.image.load("checker_pieces_drawings/red_king_p.png")
rp = pygame.image.load("checker_pieces_drawings/red_p.png")


# --------------------------------------------------
# Image resizing
# --------------------------------------------------

#changing image scale
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
        self.pieceID = pieceID
        self.piece_img = piece_img
        self.king_piece_img = king_piece_img
        self.board_x = board_x
        self.board_y = board_y
        #board_x and board_y is the top left corner position of the board
        self.square_size = square_size
        self.row = row
        self.col = col

        self.rect = self.image.get_rect(topleft=(self.board_x + self.square_size * self.col, self.board_y + self.square_size * self.row))

        self.color = None
        self.king = False

    def king_me(self):
        """King me for when a piece reaches the opposite side of the board"""
        self.king = True
        self.image = self.king_piece_img
        self.rect = self.image.get_rect(topleft=(self.board_x + self.square_size * self.col, board_y + self.square_size * self.row))

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
        self.color = piece_type

class MoveLog():
    def __init__(self):
        self.log = []

    def add_move(self, piece, row, col, new_row, new_col):
        r = self.interpert_row(row)
        nr = self.interpert_row(new_row)
        self.log.append({
            "turn": len(self.log) + 1,
            "piece": piece.pieceID,
            "action": "MOVE",
            "from": (row, col),
            "to": (new_row, new_col),
            "message" : f"{piece.pieceID}: {r}{col} -> {nr}{new_col}"
        })

    def add_captured(self, piece, captured_piece):
        self.log.append({
            "turn": len(self.log) + 1,
            "piece": piece.pieceID,
            "captured_piece" : captured_piece.pieceID,
            "action": "CAPTURED",
            "message" : f"{piece.pieceID} has captured {captured_piece.pieceID}"
        })

    def add_king(self, piece):
        self.log.append({
            "turn" : len(self.log) + 1,
            "piece" : piece.pieceID,
            "action" : "KINGED",
            "message" : f"{piece.pieceID} has been kinged"
        })

    def interpert_row(self, row):
        row_names = "ABCDEFGH"
        return row_names[row]

    def moveLog_to_CSV(self):
        df = pd.DataFrame(self.log)
        df.to_csv("Move_log.csv", index=False)


class MoveLogPanel():
    def __init__(self):
        self.scroll_offset = 0

    def handle_scroll(self, event):
        if event.type == pygame.MOUSEWHEEL or event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.scroll_offset += event.y * 20

    def draw(self, screen, move_log, font, color):
        pygame.draw.rect(screen, (40,40,40),
            (820,20,350,760))

        y = 30 + self.scroll_offset

        for entry in move_log.log:
            if 20 <= y <= 780:
                text = font.render(entry["message"], True, color)
                screen.blit(text, (830, y))
            y += 25

## ----------------------------------------------------------
# Piece Movement using checker rules
## ----------------------------------------------------------
class BoardState:
    def __init__(self, pieces):
        # ===== BOARD ARRAY: 8 rows by 8 columns, indexed as cells[row][col]. =====
        # Each cell holds its CheckerPiece, or None when the square is empty.
        # The sprites remain in their Pygame group for drawing; this grid tracks occupancy.
        self.cells = [
            [None for _ in range(BOARD_COLS)]
            for _ in range(BOARD_ROWS)
        ]
        # Red starts. A capture chain keeps the same piece active until it ends.
        self.current_player = "Red"
        self.must_continue_piece = None
        #creates move log for every board
        self.move_log = MoveLog()
        self.move_log_panel = MoveLogPanel()

        # Build the starting occupancy grid from the pieces' row and column values.
        for piece in pieces:
            self.cells[piece.row][piece.col] = piece

    def is_current_player_piece(self, piece):
        """Return whether a piece belongs to the player whose turn it is."""
        return (
            piece is not None
            and piece.pieceID.split(" ", 1)[0] == self.current_player
        )

    def get_capture_moves(self, piece):
        """Return available jump destinations for a piece."""
        if piece is None or self.cells[piece.row][piece.col] is not piece:
            return []

        if piece.king:
            row_directions = (-1, 1)
        else:
            row_directions = (1,) if piece.pieceID.startswith("Red") else (-1,)

        capture_moves = []
        piece_color = piece.pieceID.split(" ", 1)[0]
        # Check each forward diagonal (or both directions for kings) for a jump.
        for row_direction in row_directions:
            for col_direction in (-1, 1):
                middle_row = piece.row + row_direction
                middle_col = piece.col + col_direction
                target_row = piece.row + 2 * row_direction
                target_col = piece.col + 2 * col_direction
                if not (
                    0 <= target_row < BOARD_ROWS
                    and 0 <= target_col < BOARD_COLS
                ):
                    continue

                middle_piece = self.cells[middle_row][middle_col]
                target_piece = self.cells[target_row][target_col]
                if (
                    middle_piece is not None
                    and middle_piece.pieceID.split(" ", 1)[0] != piece_color
                    and target_piece is None
                ):
                    capture_moves.append((target_row, target_col))

        return capture_moves

    def move_piece(self, piece, new_row, new_col):
        """Move diagonally one step or jump an opponent on the board."""
        if piece is None:
            return False
        # Only the active color may move, and a capture chain locks the chosen piece.
        if not self.is_current_player_piece(piece):
            return False
        if self.must_continue_piece is not None and piece is not self.must_continue_piece:
            return False
        if not (0 <= new_row < BOARD_ROWS and 0 <= new_col < BOARD_COLS):
            return False
        if self.cells[piece.row][piece.col] is not piece:
            return False
        if self.cells[new_row][new_col] is not None:
            return False

        row_delta = new_row - piece.row
        col_delta = new_col - piece.col
        if abs(row_delta) != abs(col_delta) or abs(row_delta) not in (1, 2):
            return False
        if self.must_continue_piece is piece and abs(row_delta) != 2:
            return False

        captured_piece = None
        if abs(row_delta) == 2:
            middle_row = piece.row + row_delta // 2
            middle_col = piece.col + col_delta // 2
            captured_piece = self.cells[middle_row][middle_col]
            if captured_piece is None:
                return False

            piece_color = piece.pieceID.split(" ", 1)[0]
            captured_color = captured_piece.pieceID.split(" ", 1)[0]
            if piece_color == captured_color:
                return False

        # Red moves down the board, Black moves up; kings may move either way.
        if not piece.king:
            direction = 1 if piece.pieceID.startswith("Red") else -1
            if row_delta != direction * abs(row_delta):
                return False

        # Update occupancy and sprite coordinates together to keep them in sync.
        self.cells[piece.row][piece.col] = None
        if captured_piece is not None:
            middle_row = piece.row + row_delta // 2
            middle_col = piece.col + col_delta // 2
            self.cells[middle_row][middle_col] = None
            #add captured piece to move log
            self.move_log.add_captured(captured_piece)
            # Remove the captured sprite from its Pygame groups so it is no longer drawn.
            captured_piece.kill()
        self.cells[new_row][new_col] = piece
        #add movement to movelog
        self.move_log.add_move(piece, piece.row, piece.col, new_row, new_col)
        #move piece
        piece.move(new_row, new_col)


        #check new column and row and see if piece can be kinged
        if not piece.king:
            if piece.color == "Red" and new_row == BOARD_ROWS - 1:
                piece.king_me()
                piece.pieceID += "(KINGED)"
                self.move_log.add_king(piece)
            if piece.color == "Black" and new_row == 0:
                piece.king_me()
                piece.pieceID += "(KINGED)"
                self.move_log.add_king(piece)

        # Keep the turn for another available jump; otherwise hand play to the opponent.
        if captured_piece is not None and self.get_capture_moves(piece):
            self.must_continue_piece = piece
        else:
            self.must_continue_piece = None
            self.current_player = "Black" if self.current_player == "Red" else "Red"

        winner = self.check_winner()
        if winner:
            print(self.check_winner())
            self.move_log.moveLog_to_CSV()
            return winner
        
        return True

    def piece_has_moves(self, piece):
        """Checks if a piece has any available moves"""
        if self.get_capture_moves(piece):
            return True

        if piece.king:
            row_directions = (-1, 1)
        else:
            row_directions = (1,) if piece.color == "Red" else (-1,)

        for row_direction in row_directions:
            for col_direction in (-1, 1):
                t_row = piece.row + row_direction
                t_col = piece.col + col_direction

            if 0 <= t_row < BOARD_ROWS and 0 <= t_col < BOARD_COLS and self.cells[t_row][t_col] is None:
                return True

            j_row = piece.row + 2 * row_direction
            j_col = piece.col + 2 * col_direction

            if 0 <= j_row < BOARD_ROWS and 0 <= j_col < BOARD_COLS:
                middle_piece = self.cells[t_row][t_col]

                if middle_piece is not None and middle_piece.color != piece.color and self.cells[j_row][j_col] is None:
                    return True
        return False

    def get_player_pieces(self, color):
        """counts the player's pieces"""
        count = 0
        for row in self.cells:
            for piece in row:
                if piece is not None and piece.color == color:
                    count +=1
        return count

    def player_has_moves(self, color):
        """Checks if any of a player's pieces can move"""
        for piece in range(self.get_player_pieces(color)):
            if self.piece_has_moves(piece):
                return True
        return False

    def check_winner(self):
         """satisfied when a player loses all their pieces or they cannot move their pieces"""
         if self.get_player_pieces("Red") == 0 or not self.player_has_moves("Red"):
             return "Black Wins!"
         if self.get_player_pieces("Black") == 0 or not self.player_has_moves("Black"):
             return "Red Wins!"

# --------------------------------------------------
# Starting positions
# --------------------------------------------------

def create_red_pieces(piece, board_x, board_y):
    #red_piece_set = []
    red_pieces = pygame.sprite.Group()

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
                red_pieces.add(CheckerPiece("", red_piece, red_king, board_x, board_y, row, col, 46.875))
                #red_piece_set.append((piece, rect))

    for index, piece in enumerate(red_pieces):
        piece.set_pieceID(index, "Red")

    return red_pieces


def create_black_pieces(piece, board_x, board_y):
    #black_piece_set = []
    black_pieces = pygame.sprite.Group()
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
                black_pieces.add(CheckerPiece("", black_piece, black_king, board_x, board_y, row, col, 46.875))

                #black_piece_set.append((piece, rect))
    
    for index, piece in enumerate(black_pieces):
        piece.set_pieceID(index, "Black")

    return black_pieces 

#this function combines the red and black pieces into one group. this function is used in the game creation dictionary in init.py 
def create_all_pieces():
    red_piece_set = create_red_pieces(red_piece, board_x, board_y)
    black_piece_set = create_black_pieces(black_piece, board_x, board_y)

    all_pieces = pygame.sprite.Group()
    all_pieces.add(red_piece_set)
    all_pieces.add(black_piece_set)
    return all_pieces
