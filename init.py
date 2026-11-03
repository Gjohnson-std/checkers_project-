
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
    create_board,
    create_all_pieces,
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

def handle_game(event):
    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    if not session_state.network.connected or session_state.local_side is None:
        return

    x, y = event.pos

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
    old_row, old_col = selected.row, selected.col
    if not (0 <= row < 8 and 0 <= col < 8):
        navigate.selected_piece = None
        return

    selected.move(row, col)
    navigate.selected_piece = None
    if not session_state.network.send({
        "type": "move",
        "from": [old_row, old_col],
        "to": [row, col],
    }):
        selected.move(old_row, old_col)
        session_state.set_network_status(
            "Move could not be sent; connection lost."
        )


def draw_game():
    gameDisplay.blit(BOARD, (board_x, board_y))
    all_pieces.draw(gameDisplay)
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

    piece.move(to_row, to_col)
    session_state.set_network_status("Opponent moved.")


def process_network_events():
    for message in session_state.network.poll():
        message_type = message.get("type")
        if message_type == "connected":
            session_state.set_connecting(False)
            session_state.set_network_status(
                f"Opponent connected. You are {session_state.local_side}."
            )
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


def draw_build_version():
    team_text = font.render(BUILD_VER, True, BLACK_COLOR)
    gameDisplay.blit(
        team_text,
        (WIDTH - team_text.get_width() - 10, HEIGHT - team_text.get_height() - 10),
    )


## --------------------------------------------------
#  Dictionaries
# --------------------------------------------------

GAME_CREATION = {
    "board": create_board,
    "pieces": create_all_pieces
}
 #initialize the board and pieces
GAME_CREATION["board"]()
all_pieces = GAME_CREATION["pieces"]()

running = True

EVENT_HANDLERS = {
    "home": handle_home,
    "login": handle_login,
    "select_session": handle_select_session,
    "sessions": handle_session,
    "session": handle_session,
    "game": handle_game,
}

DRAW_FUNCS = {
    "home": draw_home,
    "login": draw_login,
    "select_session": draw_select_session,
    "sessions": draw_session,
    "session": draw_session,
    "game": draw_game,
}
# --------------------------------------------------
# Game loop
# --------------------------------------------------

while running:
    process_network_events()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            session_state.network.close()
            continue

        EVENT_HANDLERS[navigate.screen](event)

    gameDisplay.blit(bg, (0, 0))
    DRAW_FUNCS[navigate.screen]()
    draw_build_version()

    pygame.display.flip()


pygame.quit()
