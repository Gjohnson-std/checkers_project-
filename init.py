from pathlib import Path

import pygame

from config import BLACK_COLOR, TAN_COLOR, WHITE_COLOR
from pieces import (
    red_piece,
    black_piece,
    create_red_pieces,
    create_black_pieces
)
from credential_store import MAX_CREDENTIAL_LENGTH, save_credentials
from sessions import SessionButton, session_ID


pygame.init()


# --------------------------------------------------
# Window configuration
# --------------------------------------------------

WIDTH = 1920
HEIGHT = 1080

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Troubleshooters: Checkers Game")


# --------------------------------------------------
# Asset paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

bg_path = BASE_DIR / "Assets" / "bg.jpg"


# --------------------------------------------------
# Background
# --------------------------------------------------

bg = pygame.image.load(bg_path)
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))


# --------------------------------------------------
# Text
# --------------------------------------------------

font = pygame.font.Font(None, 25)
title_font = pygame.font.Font(None, 72)
ui_font = pygame.font.Font(None, 42)
field_font = pygame.font.Font(None, 36)
status_font = pygame.font.Font(None, 28)

BUILD_VER = "troubleshooters-cg-v0.0.1 - alpha"


# --------------------------------------------------
# Board configuration
# --------------------------------------------------

BOARD_SIZE = 375
BOARD_ROWS = 8
BOARD_COLS = 8
SQUARE_SIZE = BOARD_SIZE / BOARD_COLS

BOARD = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
board_x = (WIDTH - BOARD_SIZE) // 2
board_y = (HEIGHT - BOARD_SIZE) // 2


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
# Create board
# --------------------------------------------------

create_board()


# --------------------------------------------------
# Create pieces
# --------------------------------------------------

red_piece_set = create_red_pieces(red_piece, board_x, board_y)
black_piece_set = create_black_pieces(black_piece, board_x, board_y)

all_pieces = pygame.sprite.Group()
all_pieces.add(red_piece_set)
all_pieces.add(black_piece_set)


# --------------------------------------------------
# State
# --------------------------------------------------

running = True
screen = "home"
username = ""
password = ""
active_field = "username"
status_message = ""
selected_piece = None
selected_session = None


# --------------------------------------------------
# UI rectangles
# --------------------------------------------------

login_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2, 220, 64)
username_field = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 90, 500, 58)
password_field = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 + 4, 500, 58)
submit_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 115, 220, 58)
back_button = pygame.Rect(40, 40, 130, 52)

# field name -> rect, used for click detection and drawing
LOGIN_FIELDS = {
    "username": username_field,
    "password": password_field,
}


# --------------------------------------------------
# Session buttons
# --------------------------------------------------

session_buttons = []
start_y = HEIGHT // 2 - 40

for name in session_ID:
    rect = pygame.Rect(WIDTH // 2 - 150, start_y, 300, 50)
    session_buttons.append(SessionButton(rect, name))
    start_y += 70


# --------------------------------------------------
# Drawing helpers
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


# --------------------------------------------------
# Screen transitions
# --------------------------------------------------

def go_to(new_screen):
    """
    Single place for every screen change. Handles any setup/teardown
    a screen needs (text input on/off, clearing the login form, etc.).
    """
    global screen, username, password, active_field, status_message

    screen = new_screen

    if new_screen == "login":
        username = ""
        password = ""
        active_field = "username"
        status_message = ""
        pygame.key.start_text_input()
        return

    pygame.key.stop_text_input()


def attempt_login():
    global status_message

    if not username or not password:
        status_message = "Enter both a username and password."
        return

    try:
        save_credentials(username, password)
    except (OSError, ValueError, UnicodeDecodeError) as error:
        status_message = f"Could not save login: {error}"
        return

    status_message = "Login saved."
    go_to("session")


# --------------------------------------------------
# Home screen
# --------------------------------------------------

def handle_home(event):
    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    if login_button.collidepoint(event.pos):
        go_to("login")


def draw_home():
    draw_centered_text(
        "Troubleshooters: Checkers Game", title_font, BLACK_COLOR, HEIGHT // 2 - 130
    )
    draw_button(login_button, "login")


# --------------------------------------------------
# Login screen
# --------------------------------------------------

def login_click(event):
    global active_field

    if back_button.collidepoint(event.pos):
        go_to("home")
        return

    if submit_button.collidepoint(event.pos):
        attempt_login()
        return

    for field_name, field_rect in LOGIN_FIELDS.items():
        if field_rect.collidepoint(event.pos):
            active_field = field_name


def login_text(event):
    global username, password

    if active_field == "username":
        username += event.text[:MAX_CREDENTIAL_LENGTH - len(username)]

    if active_field == "password":
        password += event.text[:MAX_CREDENTIAL_LENGTH - len(password)]


def login_backspace():
    global username, password

    if active_field == "username":
        username = username[:-1]

    if active_field == "password":
        password = password[:-1]


def login_switch_field():
    global active_field
    active_field = "password" if active_field == "username" else "username"


# key -> action, for the login screen's KEYDOWN events
LOGIN_KEY_ACTIONS = {
    pygame.K_BACKSPACE: login_backspace,
    pygame.K_TAB: login_switch_field,
    pygame.K_RETURN: attempt_login,
}


def login_key(event):
    action = LOGIN_KEY_ACTIONS.get(event.key)
    if action:
        action()


# event type -> handler, for the login screen
LOGIN_EVENT_HANDLERS = {
    pygame.MOUSEBUTTONDOWN: login_click,
    pygame.TEXTINPUT: login_text,
    pygame.KEYDOWN: login_key,
}


def handle_login(event):
    handler = LOGIN_EVENT_HANDLERS.get(event.type)
    if handler:
        handler(event)


def draw_login():
    draw_centered_text("Login", title_font, BLACK_COLOR, HEIGHT // 2 - 230)
    draw_button(back_button, "Back")

    for rect, label, value, field_name in (
        (username_field, "Username", username, "username"),
        (password_field, "Password", "*" * len(password), "password"),
    ):
        pygame.draw.rect(gameDisplay, WHITE_COLOR, rect, border_radius=6)
        border_color = TAN_COLOR if active_field == field_name else BLACK_COLOR
        pygame.draw.rect(gameDisplay, border_color, rect, 3, border_radius=6)
        shown_text = value or label
        text_color = BLACK_COLOR if value else (110, 110, 110)
        rendered_value = field_font.render(shown_text, True, text_color)
        gameDisplay.blit(
            rendered_value,
            (rect.x + 14, rect.centery - rendered_value.get_height() // 2),
        )

    draw_button(submit_button, "Save & Play")

    if status_message:
        draw_centered_text(
            status_message, status_font, BLACK_COLOR, submit_button.bottom + 18
        )


# --------------------------------------------------
# Session screen
# --------------------------------------------------

def handle_session(event):
    global selected_session

    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    if back_button.collidepoint(event.pos):
        go_to("home")
        return

    for btn in session_buttons:
        if btn.is_clicked(event.pos):
            selected_session = btn.label
            print("Joining:", selected_session)
            go_to("game")
            return


def draw_session():
    draw_centered_text(
        "Join a Game Session", title_font, BLACK_COLOR, HEIGHT // 2 - 200
    )

    for btn in session_buttons:
        btn.draw(gameDisplay, ui_font, TAN_COLOR, BLACK_COLOR, BLACK_COLOR)

    draw_button(back_button, "Back")


# --------------------------------------------------
# Game screen
# --------------------------------------------------

def handle_game(event):
    global selected_piece

    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    x, y = event.pos

    if selected_piece is None:
        for piece in all_pieces:
            if piece.rect.collidepoint((x, y)):
                selected_piece = piece
                return
        return

    col = int((x - board_x) // SQUARE_SIZE)
    row = int((y - board_y) // SQUARE_SIZE)

    selected_piece.move(row, col)
    selected_piece = None


def draw_game():
    gameDisplay.blit(BOARD, (board_x, board_y))
    all_pieces.draw(gameDisplay)


# --------------------------------------------------
# Screen dispatch tables
# To add a screen: write handle_x / draw_x, add one line to each dict.
# --------------------------------------------------

EVENT_HANDLERS = {
    "home": handle_home,
    "login": handle_login,
    "session": handle_session,
    "game": handle_game,
}

DRAW_FUNCS = {
    "home": draw_home,
    "login": draw_login,
    "session": draw_session,
    "game": draw_game,
}


def draw_build_version():
    team_text = font.render(BUILD_VER, True, BLACK_COLOR)
    gameDisplay.blit(
        team_text,
        (WIDTH - team_text.get_width() - 10, HEIGHT - team_text.get_height() - 10),
    )


# --------------------------------------------------
# Game loop
# --------------------------------------------------

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        EVENT_HANDLERS[screen](event)

    gameDisplay.blit(bg, (0, 0))
    DRAW_FUNCS[screen]()
    draw_build_version()

    pygame.display.flip()


pygame.quit()
