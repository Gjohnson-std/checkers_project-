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
from datetime import datetime

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
            self.color = piece_type

class MoveLog():
    def __init__(self):
        """Move Log to record all moves and actions for each game"""
        self.log = []
        self.rowName = "ABCDEFGH"

    def add_move(self, piece, row, col, new_row, new_col, captured_piece, has_been_kinged):
        """Adds a move/ action to the game log"""
        message = (f"{len(self.log)+1} | MOVE {piece.pieceID}: {self.rowName[row]}{col} -> {self.rowName[new_row]}{new_col}")

        if captured_piece is not None:
            message += (f"\n\t| CAPTURE: {piece.pieceID} has taken {captured_piece.pieceID}")

        if has_been_kinged:
            message += (f"\n\t| KING: {piece.pieceID} has been kinged")
            piece.pieceID += " (KING)"

        self.log.append({
            "turn": len(self.log) + 1,
            "action": "MOVE",
            "piece": piece.pieceID,
            "from": (self.rowName[row], col),
            "to": (self.rowName[new_row], new_col),
            "captured_piece": captured_piece.pieceID if captured_piece is not None else None,
            "captured_piece_pos": (self.rowName[captured_piece.row], captured_piece.col) if captured_piece is not None else None,
            "kinged_piece": has_been_kinged,
            "message": message
        })

    def add_result(self, winner):
        """Adds the final result of the game to the move log"""
        loser = "Red" if winner == "Black" else "Black"
        self.log.append({
            "turn": len(self.log) + 1,
            "action": "GAME OVER",
            "winner": winner,
            "loser": loser,
            "message": (f"Player {winner} has won! :) \nPlayer {loser} has lost!")
        })

    def print_move_message(self):
        """Prints the messages for each action for the player"""
        if self.log:
            print(self.log[-1]["message"])

    def moveLog_to_CSV(self, fileName):
        """Turns the Log into a CSV for saving"""
        df = pd.DataFrame(self.log)
        if fileName is None:
            fileName = (f"Game_Log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        df.to_csv(fileName, index=False)

class MoveLogPanel():
    def __init__(self):
        self.self = None
        self.visable = True

        self.button_rect = pygame.Rect(900, 680, 400, 65)

    def draw(self, screen, move_log, title_font, ui_font, panel_color, color):
        if not self.visable:
            return

        panel_rect = pygame.Rect(900,20,400,650)
        pygame.draw.rect(screen, panel_color, panel_rect, border_radius=3)
        screen.set_clip(panel_rect)
        y = 60
        entries = move_log.log[-15:]
        label = title_font.render("MOVE LOG", True, color)
        screen.blit(label, (910, 30))

        for entry in entries:
            for line in entry["message"].split("\n"):
                text = ui_font.render(line, True, color)
                screen.blit(text, (920, y))
                y += 25
        screen.set_clip(None)

        #pygame.draw.rect(screen, btn_color, self.button_rect, border_radius= 3)
        #button_text = "Hide Log" if self.visable else "Show Log"
        #text_surface = title_font.render(button_text, True, (0, 0, 0))
        #screen.blit(text_surface, (self.button_rect.x, self.button_rect.y))


    def handel_moveLog_toggle(self, pos):
        if self.button_rect.collidepoint(pos):
            self.visable = not self.visable


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

        #move log
        self.moveLog = MoveLog()

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
            cap_log = captured_piece
            # Remove the captured sprite from its Pygame groups so it is no longer drawn.
            captured_piece.kill()
        self.cells[new_row][new_col] = piece
        row_log = piece.row
        col_log = piece.col
        kinged_log = False
        piece.move(new_row, new_col)

        #if piece has reached the opposite end of the board, then it will be kinged
        if not piece.king:
            if piece.color == "Red" and new_row == BOARD_ROWS - 1:
                piece.king_me()
                kinged_log = True
            if piece.color == "Black" and new_row == 0:
                piece.king_me()
                kinged_log = True
            

        #add move to the move log
        self.moveLog.add_move(piece, row_log, col_log, new_row, new_col, captured_piece, kinged_log)
        self.moveLog.print_move_message()

        # Keep the turn for another available jump; otherwise hand play to the opponent.
        if captured_piece is not None and self.get_capture_moves(piece):
            self.must_continue_piece = piece
        else:
            self.must_continue_piece = None
            self.current_player = "Black" if self.current_player == "Red" else "Red"

        winner = self.win_or_loss_check()
        if winner:
            self.moveLog.add_result(winner)
            self.moveLog.print_move_message()
            self.moveLog.moveLog_to_CSV(None)

        return True

    def piece_count(self, player_color):
        """Gets the remaining piece count from the board after each turn"""
        count = 0
        #checks each row for remaining pieces from check player
        for row in self.cells:
            for piece in row:
                if piece is not None and piece.color == player_color:
                    count += 1
        return count

    def get_remaining_pieces(self, player_color):
            """Gets the remaining piece count from the board after each turn"""
            remaining = []
            #checks each row for remaining pieces from check player
            for row in self.cells:
                for piece in row:
                    if piece is not None and piece.color == player_color:
                        remaining.append(piece)
            return remaining

   
    def piece_has_moves(self, piece):
        if self.get_capture_moves(piece):
            #if there are capture moves then there are valid moves
            return True

        if piece.king:
            #king checks four spaces diagonally
            row_directions = (-1, 1)
        else:
            #piece checks two spaces foward only
            row_directions = (1,) if piece.color == "Red" else (-1,)

        for row_direction in row_directions:
            for col_direction in (1, -1):
                row = piece.row + row_direction
                col = piece.col + col_direction

                if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS and self.cells[row][col] is None:
                    #True if any near valid board space is empty
                    return True

                jump_row = piece.row + 2 * row_direction
                jump_col = piece.col + 2 * col_direction

                if 0 <= jump_row < BOARD_ROWS and 0 <= jump_col < BOARD_COLS:
                    middle_piece = self.cells[row][col]

                    if middle_piece is not None and middle_piece.color != piece.color and self.cells[jump_row][jump_col] is not None:
                        #True if the piece can make a valid jump over another piece
                        return True
                    
        return False

    def player_has_moves(self, player_color):
        """checks each of a player's remaining pieces to see if they have any available moves"""
        for piece in self.get_remaining_pieces(player_color):
            if self.piece_has_moves(piece):
                return True
        return False

    def win_or_loss_check(self):
        """Checks if a player has won or lost each turn"""
        #win and loss condition based on which player looses all of their pieces first
        if self.piece_count("Red") == 0:
            return "Black"
        if self.piece_count("Black") == 0:
            return "Red"
        if not self.player_has_moves("Red"):
            return "Black"
        if not self.player_has_moves("Black"):
            return "Red"


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