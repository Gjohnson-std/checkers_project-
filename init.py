
import pygame
pygame.init()

from config import WIDTH, HEIGHT 
# --------------------------------------------------
# Window configuration
# --------------------------------------------------

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Troubleshooters: Checkers Game")


from config import (
    WIDTH,
    HEIGHT,
    BOARD_SIZE,
    board_y,
    TAN_COLOR,
    BLACK_COLOR,
    WHITE_COLOR,
    SQUARE_SIZE,
    board_x,
    board_y,
    font,
    title_font,
    ui_font,
    field_font,
    status_font,
    BUILD_VER,
    bg,
    back_button,
)


import navigate
import sessions as session_state

from board import (
    BOARD,
    BoardState,
    create_board,
    create_all_pieces,
    MoveLogPanel,
    GameOverPanel
)


from home import (
    handle_home,
    title_bg,
    title_img,
    login_img,
    settings_img,
    exit_img,
    title_rect,
    login_rect,
    settings_rect,
    exit_rect,
)

from login import (
    handle_login,
    username_field,
    password_field,
    submit_button,
)

from select_session import (
    handle_session_click,
    session_load_screen,
)

from sessions import handle_session
from sessions import (
    handle_session,
    session_buttons,
)
from restart import RestartVote

from hud import HUD

from computer_player import handle_difficulty, draw_difficulty, take_computer_turn
from victory_screen import VictoryScreen
# --------------------------------------------------
# Drawing helpers -- all of these functions use varible game.Display.bilt and they have to stay in init. It'll crash if i remove them
# --------------------------------------------------

def draw_centered_text(text, text_font, color, y):
    rendered_text = text_font.render(text, True, color)
    gameDisplay.blit(
        rendered_text,
        (WIDTH // 2 - rendered_text.get_width() // 2, y),
    )


def draw_button(rect, label):
    pygame.draw.rect(gameDisplay, TAN_COLOR, rect, border_radius=8)
    pygame.draw.rect(gameDisplay, BLACK_COLOR, rect, 3, border_radius=8)
    rendered_label = ui_font.render(label, True, BLACK_COLOR)
    gameDisplay.blit(
        rendered_label,
        (
            rect.centerx - rendered_label.get_width() // 2,
            rect.centery - rendered_label.get_height() // 2,
        ),
    )



def draw_home():
    gameDisplay.blit(title_bg, (0, 0))
    gameDisplay.blit(title_img, title_rect)
    gameDisplay.blit(login_img, login_rect)
    gameDisplay.blit(settings_img, settings_rect)
    gameDisplay.blit(exit_img, exit_rect)



def draw_login():
    draw_centered_text("Login", title_font, BLACK_COLOR, HEIGHT // 2 - 230)
    draw_button(back_button, "Back")

    for rect, label, value, field_name in (
        (username_field, "Username", navigate.username, "username"),
        (password_field, "Password", "*" * len(navigate.password), "password"),
    ):
        pygame.draw.rect(gameDisplay, WHITE_COLOR, rect, border_radius=6)

        border_color = (
            TAN_COLOR
            if navigate.active_field == field_name
            else BLACK_COLOR
        )

        pygame.draw.rect(gameDisplay, border_color, rect, 3, border_radius=6)

        shown_text = value or label
        text_color = BLACK_COLOR if value else (110, 110, 110)
        rendered_value = field_font.render(shown_text, True, text_color)

        gameDisplay.blit(
            rendered_value,
            (rect.x + 14, rect.centery - rendered_value.get_height() // 2),
        )

    draw_button(submit_button, "Save & Play")

    if navigate.status_message:
        draw_centered_text(
            navigate.status_message,
            status_font,
            BLACK_COLOR,
            submit_button.bottom + 18,
        )



def draw_session():
    session_state.draw_session(gameDisplay)


def draw_select_session():
    session_load_screen(gameDisplay, title_font, ui_font)


def handle_select_session(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        handle_session_click(event)


# --------------------------------------------------
# Game screen
# --------------------------------------------------

restart_vote = RestartVote()
restart_yes_button = pygame.Rect(WIDTH // 2 - 155, HEIGHT // 2 + 38, 140, 50)
restart_no_button = pygame.Rect(WIDTH // 2 + 15, HEIGHT // 2 + 38, 140, 50)

hud = HUD()

victory_screen = None

def reset_game():
    global all_pieces, board_state

    GAME_CREATION["board"]()
    all_pieces = GAME_CREATION["pieces"]()
    board_state = BoardState(all_pieces)
    navigate.selected_piece = None
    restart_vote.cancel()

def handle_restart_choice(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        restart_vote.cancel()
        return

    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    if restart_yes_button.collidepoint(event.pos):
        if restart_vote.stage == "confirm":
            if navigate.game_mode == "computer":
                reset_game()
            else:
                restart_vote.confirm(True)
        elif restart_vote.vote(True):
            reset_game()
        return

    if restart_no_button.collidepoint(event.pos):
        if restart_vote.stage == "confirm":
            restart_vote.confirm(False)
        elif restart_vote.stage == "vote":
            restart_vote.vote(False)
        return


def handle_game(event):
    if restart_vote.stage is not None:
        handle_restart_choice(event)
        return

    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        restart_vote.request()
        return

    if navigate.game_mode == "computer" and board_state.current_player == "Black":
        return

    if board_state.get_winner() is not None:
            return
    
    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    if not session_state.network.connected or session_state.local_side is None:
        session_state.set_network_status("Connect to an opponent before moving.")
        return
    #toggle move log panel on and off

    if move_log_panel.button_rect.collidepoint(event.pos):
        move_log_panel.visable = not move_log_panel.visable
        return

    if board_state.game_over:
        game_over_panel.visable = True
        if game_over_panel.save_log_button.collidepoint(event.pos):
            board_state.moveLog.moveLog_to_CSV(None)
        elif game_over_panel.new_game_button.collidepoint(event.pos):
            reset_game()
        elif game_over_panel.exit_game_button.collidepoint(event.pos):
            pygame.quit()
        return

    x, y = event.pos
    board_col_x = x - board_x
    board_row_y = y - board_y
    if not (0 <= board_col_x < BOARD_SIZE and 0 <= board_row_y < BOARD_SIZE):
        return

    if navigate.selected_piece is None:
        for piece in all_pieces:
            if (
                piece.rect.collidepoint((x, y))
                and piece.pieceID.startswith(f"{session_state.local_side} ")
            ):
                navigate.selected_piece = piece
                return
        return

    col = int((x - board_x) // SQUARE_SIZE)
    row = int((y - board_y) // SQUARE_SIZE)
    selected = navigate.selected_piece
    if not (0 <= row < 8 and 0 <= col < 8):
        navigate.selected_piece = None
        return

    col = int(board_col_x // SQUARE_SIZE)
    row = int(board_row_y // SQUARE_SIZE)
    clicked_piece = board_state.cells[row][col]

    if board_state.must_continue_piece is not None:
        # A capture chain cannot be interrupted by selecting another piece.
        navigate.selected_piece = board_state.must_continue_piece
        if clicked_piece is None:
            piece = navigate.selected_piece
            old_row, old_col = piece.row, piece.col
            if board_state.move_piece(piece, row, col):
                navigate.selected_piece = board_state.must_continue_piece
                board_state.refresh()
                if not session_state.network.send({
                    "type": "move",
                    "from": [old_row, old_col],
                    "to": [row, col],
                }):
                    session_state.set_network_status(
                        "Move could not be sent; connection lost."
                    )
        return

    if clicked_piece is not None:
        # Only the active player can choose a piece; the model checks moves again.
        if board_state.is_current_player_piece(clicked_piece):
            navigate.selected_piece = (
                None if clicked_piece is navigate.selected_piece else clicked_piece
            )
        else:
            navigate.selected_piece = None
        return

    if navigate.selected_piece is not None:
        piece = navigate.selected_piece
        old_row, old_col = piece.row, piece.col
        if board_state.move_piece(piece, row, col):
            navigate.selected_piece = board_state.must_continue_piece
            board_state.refresh()
            if not session_state.network.send({
                "type": "move",
                "from": [old_row, old_col],
                "to": [row, col],
            }):
                session_state.set_network_status(
                    "Move could not be sent; connection lost."
                )


def draw_game():
    gameDisplay.blit(BOARD, (board_x, board_y))
    all_pieces.draw(gameDisplay)
    # Draw HUD added 
    hud.draw(gameDisplay, board_state)
    status = status_font.render(
        session_state.status_message,
        True,
        BLACK_COLOR,
    )
    gameDisplay.blit(status, status.get_rect(center=(WIDTH // 2, board_y - 24)))


def apply_remote_move(data):
    if not isinstance(data, dict) or data.get("type") != "move":
        session_state.set_network_status(
            "Received an unsupported network message."
        )
        return

    origin = data.get("from")
    destination = data.get("to")
    if (
        not isinstance(origin, list)
        or not isinstance(destination, list)
        or len(origin) != 2
        or len(destination) != 2
        or any(type(value) is not int for value in origin + destination)
    ):
        session_state.set_network_status("Received an invalid move.")
        return

    from_row, from_col = origin
    to_row, to_col = destination
    if any(not 0 <= value < 8 for value in (from_row, from_col, to_row, to_col)):
        session_state.set_network_status("Received an out-of-board move.")
        return

    opponent_side = "Black" if session_state.local_side == "Red" else "Red"
    piece = next(
        (
            candidate
            for candidate in all_pieces
            if candidate.row == from_row
            and candidate.col == from_col
            and candidate.pieceID.startswith(f"{opponent_side} ")
        ),
        None,
    )
    if piece is None:
        session_state.set_network_status(
            "Received a move for a piece that is not available."
        )
        return

    board_state.current_player = opponent_side
    if board_state.move_piece(piece, to_row, to_col):
        board_state.refresh()
        session_state.set_network_status("Opponent moved.")
    else:
        session_state.set_network_status("Received an invalid opponent move.")


def process_network_events():
    for message in session_state.network.poll():
        message_type = message.get("type")
        if message_type == "connected":
            session_state.set_connecting(False)
            session_state.set_network_status(
                f"Opponent connected. You are {session_state.local_side}."
            )
            # Added this line to only start  HUD timer once opponent has connected
            hud.startTimer(board_state)

            if session_state.local_side == "Black":
                navigate.go_to("game")
        elif message_type == "message":
            apply_remote_move(message.get("data"))
        elif message_type == "disconnected":
            session_state.set_network_status("Opponent disconnected.")
            session_state.network.close()
        elif message_type == "error":
            session_state.set_connecting(False)
            session_state.set_network_status(
                f"Network error: {message.get('message', 'unknown error')}"
            )
    button_text = "Hide Log" if move_log_panel.visable else "Show Log"
    draw_button(move_log_panel.button_rect, button_text)
    move_log_panel.draw(gameDisplay, board_state.moveLog, ui_font, font, WHITE_COLOR, BLACK_COLOR)
    game_over_panel.draw(gameDisplay, board_state, ui_font, font, WHITE_COLOR, BLACK_COLOR)
    game_over_panel.visable = board_state.game_over
    if game_over_panel.visable:
        draw_button(game_over_panel.save_log_button, "Save Game Log")
        draw_button(game_over_panel.new_game_button, "New Game")
        draw_button(game_over_panel.exit_game_button, "Exit Game")



# --------------------------------------------------
# Victory screen
# --------------------------------------------------
def show_victory(player_won=True):
    global victory_screen

    if victory_screen is not None:
        return

    gameDisplay.blit(bg, (0, 0))
    draw_game()

    victory_screen = VictoryScreen(
        gameDisplay,
        player_won=player_won
    )

    navigate.go_to("victory")


def handle_victory(event):
    global victory_screen

    if victory_screen is None:
        return

    result = victory_screen.handle_event(event)

    if result == "select_sessions":
        reset_game()
        navigate.selected_session = None
        navigate.game_mode = "multiplayer"
        navigate.new_game_requested = False
        victory_screen = None
        navigate.go_to("select_session")

    elif result == "main_menu":
        reset_game()
        navigate.game_mode = "multiplayer"
        navigate.new_game_requested = False
        victory_screen = None
        navigate.go_to("home")


def draw_victory():
    if victory_screen is not None:
        victory_screen.draw()

    # --------------------------------------------------
    # Display Win / Loss
    # --------------------------------------------------

    winner = board_state.get_winner()

    if winner is not None:
        if navigate.game_mode == "computer":
            message = (
                "You Win!" if winner == "Red"
                else "Computer Wins!"
            )
        else:
            message = f"{winner} Wins!"

        draw_centered_text(
            message,
            title_font,
            BLACK_COLOR,
            max(10, board_y - 90)
        )

    if navigate.game_mode == "computer":
        draw_centered_text("Vs Computer - " + navigate.computer_difficulty.title(),status_font, BLACK_COLOR, max(10, board_y - 45))

    if restart_vote.stage is not None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        gameDisplay.blit(overlay, (0, 0))

        dialog = pygame.Rect(WIDTH // 2 - 280, HEIGHT // 2 - 95, 560, 200)
        pygame.draw.rect(gameDisplay, TAN_COLOR, dialog, border_radius=10)
        pygame.draw.rect(gameDisplay, BLACK_COLOR, dialog, 3, border_radius=10)

        prompt = (
            "Do you want to restart?"
            if restart_vote.stage == "confirm"
            else "Your opponent requested a restart. Do you agree?"
        )
        draw_centered_text(prompt, status_font, BLACK_COLOR, dialog.y + 35)
        draw_button(restart_yes_button, "Yes")
        draw_button(restart_no_button, "No")


def draw_build_version():
    team_text = font.render(BUILD_VER, True, BLACK_COLOR)
    gameDisplay.blit(
        team_text,
        (WIDTH - team_text.get_width() - 10, HEIGHT - team_text.get_height() - 10),
    )

def reset_game():
    global all_pieces
    global board_state
    global move_log_panel
    global game_over_panel
    all_pieces = create_all_pieces()
    board_state = BoardState(all_pieces)
    move_log_panel.visible = True
    game_over_panel.visible = False
    navigate.selected_piece = None

## --------------------------------------------------
#  Dictionaries
# --------------------------------------------------

GAME_CREATION = {
    "board": create_board,
    "pieces": create_all_pieces,
    "move_log": MoveLogPanel(),
    "game_over": GameOverPanel()
}
 #initialize the board and pieces
GAME_CREATION["board"]()
all_pieces = GAME_CREATION["pieces"]()
board_state = BoardState(all_pieces)
move_log_panel = GAME_CREATION["move_log"]
game_over_panel = GAME_CREATION["game_over"]

running = True

EVENT_HANDLERS = {
    "home": handle_home,
    "login": handle_login,
    "select_session": handle_select_session,
    "computer_difficulty": handle_difficulty,
    "sessions": handle_session,
    "session": handle_session,
    "game": handle_game,
    "victory": handle_victory,
}

DRAW_FUNCS = {
    "home": draw_home,
    "login": draw_login,
    "select_session": draw_select_session,
    "computer_difficulty": lambda: draw_difficulty(gameDisplay, title_font, ui_font),
    "sessions": draw_session,
    "session": draw_session,
    "game": draw_game,
    "victory": draw_victory
}
# --------------------------------------------------
# Game loop
# --------------------------------------------------

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            session_state.network.close()
            continue

        handler = EVENT_HANDLERS.get(navigate.screen)
        if handler is not None:
            handler(event)

    if navigate.new_game_requested:
        reset_game()
        navigate.new_game_requested = False

    if (
        navigate.screen == "game"
        and navigate.game_mode == "computer"
        and restart_vote.stage is None
        and board_state.current_player == "Black"
        and board_state.get_winner() is None
    ):
        take_computer_turn(
            board_state,
            navigate.computer_difficulty
        )

    # Trigger only after a completed human win
    # against the computer.
    if (
        navigate.screen == "game"
        and navigate.game_mode == "computer"
    ):
        winner = board_state.get_winner()

        if winner == "Red":
            show_victory(player_won=True)
        elif winner == "Black":
            show_victory(player_won=False)
        
    if navigate.screen == "victory":
        draw_victory()
    else:
        gameDisplay.blit(bg, (0, 0))
        draw = DRAW_FUNCS.get(navigate.screen)

        if draw is not None:
            draw()

        draw_build_version()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
