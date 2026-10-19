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

red_piece_set = create_red_pieces(
    red_piece,
    board_x,
    board_y
)

black_piece_set = create_black_pieces(
    black_piece,
    board_x,
    board_y
)


# --------------------------------------------------
# Screen configuration
# --------------------------------------------------

running = True
screen = "home"

username = ""
password = ""

active_field = "username"
status_message = ""

selected_session = None
selected_piece = None


# --------------------------------------------------
# Button configuration
# --------------------------------------------------

login_button = pygame.Rect(
    WIDTH // 2 - 110,
    HEIGHT // 2,
    220,
    64
)

username_field = pygame.Rect(
    WIDTH // 2 - 250,
    HEIGHT // 2 - 90,
    500,
    58
)

password_field = pygame.Rect(
    WIDTH // 2 - 250,
    HEIGHT // 2 + 4,
    500,
    58
)

submit_button = pygame.Rect(
    WIDTH // 2 - 110,
    HEIGHT // 2 + 115,
    220,
    58
)

back_button = pygame.Rect(
    40,
    40,
    130,
    52
)


# --------------------------------------------------
# Session joining
# --------------------------------------------------

session_buttons = []

start_y = HEIGHT // 2 - 40

for name in session_ID:

    rect = pygame.Rect(
        WIDTH // 2 - 150,
        start_y,
        300,
        50
    )

    session_buttons.append(
        SessionButton(rect, name)
    )

    start_y += 70


# --------------------------------------------------
# Piece selection
# --------------------------------------------------

all_pieces = pygame.sprite.Group()

all_pieces.add(red_piece_set)
all_pieces.add(black_piece_set)


# --------------------------------------------------
# Login functions
# --------------------------------------------------

def attempt_login():
    global screen, status_message

    if not username or not password:
        status_message = "Enter both a username and password."
        return

    try:
        save_credentials(username, password)

    except (OSError, ValueError, UnicodeDecodeError) as error:
        status_message = f"Could not save login: {error}"
        return

    status_message = "Login saved."

    screen = "session"

    pygame.key.stop_text_input()


# --------------------------------------------------
# Drawing helper functions
# --------------------------------------------------

def draw_centered_text(text, text_font, color, y):

    rendered_text = text_font.render(
        text,
        True,
        color
    )

    gameDisplay.blit(
        rendered_text,
        (
            WIDTH // 2 - rendered_text.get_width() // 2,
            y
        )
    )


def draw_button(rect, label):

    pygame.draw.rect(
        gameDisplay,
        TAN_COLOR,
        rect,
        border_radius=8
    )

    pygame.draw.rect(
        gameDisplay,
        BLACK_COLOR,
        rect,
        3,
        border_radius=8
    )

    rendered_label = ui_font.render(
        label,
        True,
        BLACK_COLOR
    )

    gameDisplay.blit(
        rendered_label,
        (
            rect.centerx - rendered_label.get_width() // 2,
            rect.centery - rendered_label.get_height() // 2
        )
    )


# --------------------------------------------------
# Home screen event handler
# --------------------------------------------------

def handle_home_event(event):
    global screen, username, password
    global active_field, status_message

    if event.type == pygame.MOUSEBUTTONDOWN:

        if login_button.collidepoint(event.pos):

            screen = "login"

            username = ""
            password = ""

            active_field = "username"
            status_message = ""

            pygame.key.start_text_input()


# --------------------------------------------------
# Login screen event handler
# --------------------------------------------------

def handle_login_event(event):
    global screen, username, password, active_field

    if event.type == pygame.MOUSEBUTTONDOWN:

        if back_button.collidepoint(event.pos):

            screen = "home"

            pygame.key.stop_text_input()

        elif username_field.collidepoint(event.pos):

            active_field = "username"

        elif password_field.collidepoint(event.pos):

            active_field = "password"

        elif submit_button.collidepoint(event.pos):

            attempt_login()

    elif event.type == pygame.TEXTINPUT:

        if active_field == "username":

            if len(username) < MAX_CREDENTIAL_LENGTH:

                username += event.text[
                    :MAX_CREDENTIAL_LENGTH - len(username)
                ]

        elif active_field == "password":

            if len(password) < MAX_CREDENTIAL_LENGTH:

                password += event.text[
                    :MAX_CREDENTIAL_LENGTH - len(password)
                ]

    elif event.type == pygame.KEYDOWN:

        if event.key == pygame.K_BACKSPACE:

            if active_field == "username":
                username = username[:-1]

            else:
                password = password[:-1]

        elif event.key == pygame.K_TAB:

            active_field = (
                "password" if active_field == "username"
                else "username"
            )

        elif event.key == pygame.K_RETURN:

            attempt_login()


# --------------------------------------------------
# Session screen event handler
# --------------------------------------------------

def handle_session_event(event):
    global screen, selected_session

    if event.type == pygame.MOUSEBUTTONDOWN:

        if back_button.collidepoint(event.pos):

            screen = "home"

        else:

            for btn in session_buttons:

                if btn.is_clicked(event.pos):

                    selected_session = btn.label

                    print("Joining:", selected_session)

                    screen = "game"

                    break


# --------------------------------------------------
# Game screen event handler
# --------------------------------------------------

def handle_game_event(event):
    global selected_piece

    if event.type == pygame.MOUSEBUTTONDOWN:

        x, y = event.pos

        if selected_piece is None:

            for piece in all_pieces:

                if piece.rect.collidepoint((x, y)):

                    selected_piece = piece

                    break

        else:

            col = int((x - board_x) // SQUARE_SIZE)
            row = int((y - board_y) // SQUARE_SIZE)

            selected_piece.move(row, col)

            selected_piece = None


# --------------------------------------------------
# Home screen drawing
# --------------------------------------------------

def draw_home_screen():

    draw_centered_text(
        "Troubleshooters: Checkers Game",
        title_font,
        BLACK_COLOR,
        HEIGHT // 2 - 130
    )

    draw_button(
        login_button,
        "login"
    )


# --------------------------------------------------
# Login screen drawing
# --------------------------------------------------

def draw_login_screen():

    draw_centered_text(
        "Login",
        title_font,
        BLACK_COLOR,
        HEIGHT // 2 - 230
    )

    draw_button(
        back_button,
        "Back"
    )

    for rect, label, value, field_name in (
        (username_field, "Username", username, "username"),
        (password_field, "Password", "*" * len(password), "password"),
    ):

        pygame.draw.rect(
            gameDisplay,
            WHITE_COLOR,
            rect,
            border_radius=6
        )

        border_color = (
            TAN_COLOR if active_field == field_name
            else BLACK_COLOR
        )

        pygame.draw.rect(
            gameDisplay,
            border_color,
            rect,
            3,
            border_radius=6
        )

        shown_text = value or label

        text_color = (
            BLACK_COLOR if value
            else (110, 110, 110)
        )

        rendered_value = field_font.render(
            shown_text,
            True,
            text_color
        )

        gameDisplay.blit(
            rendered_value,
            (
                rect.x + 14,
                rect.centery - rendered_value.get_height() // 2
            )
        )

    draw_button(
        submit_button,
        "Save & Play"
    )

    if status_message:

        draw_centered_text(
            status_message,
            status_font,
            BLACK_COLOR,
            submit_button.bottom + 18
        )


# --------------------------------------------------
# Session screen drawing
# --------------------------------------------------

def draw_session_screen():

    draw_centered_text(
        "Join a Game Session",
        title_font,
        BLACK_COLOR,
        HEIGHT // 2 - 200
    )

    for btn in session_buttons:

        btn.draw(
            gameDisplay,
            ui_font,
            TAN_COLOR,
            BLACK_COLOR,
            BLACK_COLOR
        )

    draw_button(
        back_button,
        "Back"
    )


# --------------------------------------------------
# Game screen drawing
# --------------------------------------------------

def draw_game_screen():

    gameDisplay.blit(
        BOARD,
        (board_x, board_y)
    )

    red_piece_set.draw(gameDisplay)
    black_piece_set.draw(gameDisplay)


# --------------------------------------------------
# Screen registry
# --------------------------------------------------

screens = {
    "home": {
        "event": handle_home_event,
        "draw": draw_home_screen
    },

    "login": {
        "event": handle_login_event,
        "draw": draw_login_screen
    },

    "session": {
        "event": handle_session_event,
        "draw": draw_session_screen
    },

    "game": {
        "event": handle_game_event,
        "draw": draw_game_screen
    }
}


# --------------------------------------------------
# Game loop
# --------------------------------------------------

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        else:

            screens[screen]["event"](event)

    # Draw background
    gameDisplay.blit(bg, (0, 0))

    # Draw current screen
    screens[screen]["draw"]()

    # Draw version text on every screen
    team_text = font.render(
        BUILD_VER,
        True,
        BLACK_COLOR
    )

    gameDisplay.blit(
        team_text,
        (
            WIDTH - team_text.get_width() - 10,
            HEIGHT - team_text.get_height() - 10
        )
    )

    pygame.display.flip()


pygame.quit()