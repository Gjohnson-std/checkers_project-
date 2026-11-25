"""Computer checkers opponent and difficulty selection UI.

The AI uses a lightweight immutable board snapshot for searching, but commits
moves through the game's existing BoardState.move_piece implementation.
"""
import random
import pygame
import navigate
from navigate import go_to
from config import WIDTH, HEIGHT, BLACK_COLOR, TAN_COLOR, back_button

DIFFICULTIES = {"easy": 0, "medium": 1, "hard": 3}
COMPUTER_COLOR = "Black"
HUMAN_COLOR = "Red"

DIFFICULTY_BUTTONS = {
    level: pygame.Rect(WIDTH // 2 - 180, HEIGHT // 2 - 70 + index * 80, 360, 60)
    for index, level in enumerate(DIFFICULTIES)
}


def select_difficulty(level):
    if level not in DIFFICULTIES:
        raise ValueError("Unknown computer difficulty")
    navigate.game_mode = "computer"
    navigate.computer_difficulty = level
    navigate.new_game_requested = True
    go_to("game")


def handle_difficulty(event):
    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return
    if back_button.collidepoint(event.pos):
        go_to("select_session")
        return
    for level, rect in DIFFICULTY_BUTTONS.items():
        if rect.collidepoint(event.pos):
            select_difficulty(level)
            return


def draw_difficulty(surface, title_font, button_font):
    heading = title_font.render("Computer Difficulty", True, BLACK_COLOR)
    surface.blit(heading, heading.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 165)))
    for level, rect in DIFFICULTY_BUTTONS.items():
        pygame.draw.rect(surface, TAN_COLOR, rect, border_radius=8)
        pygame.draw.rect(surface, BLACK_COLOR, rect, 3, border_radius=8)
        label = button_font.render(level.title(), True, BLACK_COLOR)
        surface.blit(label, label.get_rect(center=rect.center))
    pygame.draw.rect(surface, TAN_COLOR, back_button, border_radius=8)
    pygame.draw.rect(surface, BLACK_COLOR, back_button, 3, border_radius=8)
    label = button_font.render("Back", True, BLACK_COLOR)
    surface.blit(label, label.get_rect(center=back_button.center))

def start_computer_game(difficulty):
    navigate.game_mode = "computer"
    navigate.computer_difficulty = difficulty
    navigate.new_game_requested = True
    go_to("game")

def snapshot(board_state):
    """Represent each piece as (color, is_king), or None."""
    return tuple(tuple(
        None if piece is None else (piece.pieceID.split(" ", 1)[0], piece.king)
        for piece in row
    ) for row in board_state.cells)


def moves_for_piece(board, row, col, captures_only=False):
    item = board[row][col]
    if item is None:
        return []
    color, king = item
    directions = (-1, 1) if king else ((1,) if color == "Red" else (-1,))
    captures, steps = [], []
    for dr in directions:
        for dc in (-1, 1):
            nr, nc = row + dr, col + dc
            if not (0 <= nr < 8 and 0 <= nc < 8):
                continue
            if board[nr][nc] is None:
                steps.append((row, col, nr, nc))
            elif board[nr][nc][0] != color:
                jr, jc = nr + dr, nc + dc
                if 0 <= jr < 8 and 0 <= jc < 8 and board[jr][jc] is None:
                    captures.append((row, col, jr, jc))
    return captures if captures_only else captures + steps


def legal_moves(board, color, forced=None):
    if forced is not None:
        r, c = forced
        return [m for m in moves_for_piece(board, r, c, True) if abs(m[2] - r) == 2]
    return [move for row in range(8) for col in range(8)
            if board[row][col] is not None and board[row][col][0] == color
            for move in moves_for_piece(board, row, col)]


def apply_move(board, move):
    sr, sc, tr, tc = move
    rows = [list(row) for row in board]
    color, king = rows[sr][sc]
    rows[sr][sc] = None
    if abs(tr - sr) == 2:
        rows[(sr + tr) // 2][(sc + tc) // 2] = None
    # Existing BoardState does not automatically crown pieces; mirror that rule.
    rows[tr][tc] = (color, king)
    result = tuple(tuple(row) for row in rows)
    forced = (tr, tc) if abs(tr - sr) == 2 and moves_for_piece(result, tr, tc, True) else None
    return result, forced


def evaluate(board):
    score = 0
    for row_index, row in enumerate(board):
        for col_index, piece in enumerate(row):
            if piece is None:
                continue
            color, king = piece
            value = (175 if king else 100) + (7 if 2 <= col_index <= 5 else 0)
            if not king:
                value += (7 - row_index if color == "Black" else row_index) * 3
            score += value if color == COMPUTER_COLOR else -value
    return score


def search(board, color, depth, forced=None, alpha=-float("inf"), beta=float("inf")):
    moves = legal_moves(board, color, forced)
    if not moves:
        return ((-100000 if color == COMPUTER_COLOR else 100000), None)
    if depth <= 0 and forced is None:
        return evaluate(board), None
    maximizing = color == COMPUTER_COLOR
    best_score = -float("inf") if maximizing else float("inf")
    best_move = None
    for move in moves:
        next_board, next_forced = apply_move(board, move)
        next_color = color if next_forced else (HUMAN_COLOR if maximizing else COMPUTER_COLOR)
        score, _ = search(next_board, next_color, depth if next_forced else max(0, depth - 1),
                          next_forced, alpha, beta)
        if (score > best_score if maximizing else score < best_score):
            best_score, best_move = score, move
        if maximizing:
            alpha = max(alpha, best_score)
        else:
            beta = min(beta, best_score)
        if beta <= alpha:
            break
    return best_score, best_move


def choose_move(board_state, difficulty):
    board = snapshot(board_state)
    forced_piece = board_state.must_continue_piece
    forced = (forced_piece.row, forced_piece.col) if forced_piece is not None else None
    moves = legal_moves(board, COMPUTER_COLOR, forced)
    if not moves:
        return None
    if difficulty == "easy":
        return random.choice(moves)
    if difficulty == "medium":
        # Prefer captures, then safer and more central positions.
        return max(moves, key=lambda m: (abs(m[2] - m[0]) == 2,
                                        evaluate(apply_move(board, m)[0]) + random.random() * 15))
    if difficulty == "hard":
        return search(board, COMPUTER_COLOR, DIFFICULTIES["hard"], forced)[1]
    raise ValueError("Unknown difficulty")


def take_computer_turn(board_state, difficulty):
    """Make one move; call again while a forced capture chain remains."""
    if board_state.current_player != COMPUTER_COLOR:
        return False
    move = choose_move(board_state, difficulty)
    if move is None:
        return False
    sr, sc, tr, tc = move
    return board_state.move_piece(board_state.cells[sr][sc], tr, tc)
