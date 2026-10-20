from pathlib import Path
import pygame
from config import BLACK_COLOR, TAN_COLOR, WHITE_COLOR
from pieces import ( red_piece, black_piece, create_red_pieces, create_black_pieces)
from credential_store import MAX_CREDENTIAL_LENGTH, save_credentials
from sessions import SessionButton, session_ID
from select_session import host_game_button, join_session_button, session_load_screen
from home import run_home_screen


pygame.init()


# --------------------------------------------------
# Window configuration
# --------------------------------------------------

WIDTH = 800
HEIGHT = 600

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


BUILD_VER = "troubleshooters-cg-v0.0.1 - alpha"


# --------------------------------------------------
# Board configuration
# --------------------------------------------------

BOARD_SIZE = 375
BOARD_ROWS = 8
BOARD_COLS = 8
SQUARE_SIZE = BOARD_SIZE / BOARD_COLS

BOARD = pygame.Surface((BOARD_SIZE, BOARD_SIZE))


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

red_piece_set = create_red_pieces(red_piece)
black_piece_set = create_black_pieces(black_piece)


# --------------------------------------------------
# Game loop
# --------------------------------------------------

running = True
screen = "home"
username = ""
password = ""
active_field = "username"
status_message = ""

username_field = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 90, 500, 58)
password_field = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 + 4, 500, 58)
submit_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 115, 220, 58)
back_button = pygame.Rect(40, 40, 130, 52)

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    status_message = "Login saved."
    screen = "session_select"  # Navigate to the session selection screen after login
    pygame.key.stop_text_input()

def draw_centered_text(text, text_font, color, y):
    rendered_text = text_font.render(text, True, color)
    gameDisplay.blit(
        rendered_text,
        (WIDTH // 2 - rendered_text.get_width() // 2, y),
    )

    gameDisplay.blit(
        team_text,
        (
            WIDTH - team_text.get_width() - 10,
            HEIGHT - team_text.get_height() - 10
        )
    )

#-----------------------------------------------------
#Session Joining
session_buttons = []
start_y = HEIGHT // 2 - 40

for name in session_ID:
    rect = pygame.Rect(WIDTH // 2 - 150, start_y, 300, 50)
    session_buttons.append(SessionButton(rect, name))
    start_y += 70

#-----------------------------------------------------
all_pieces = pygame.sprite.Group()
all_pieces.add(red_piece_set)
all_pieces.add(black_piece_set)
selected_piece = None

while running:
    if screen == "home":
        result = run_home_screen(gameDisplay)
        if result == "login":
            screen = "login"
            username = ""
            password = ""
            active_field = "username"
            status_message = ""
            pygame.key.start_text_input()
        elif result == "settings":
            screen = "settings"
        elif result == "exit":
            running = False
        continue

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif screen == "login" and event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                screen = "home"
                pygame.key.stop_text_input()
            elif username_field.collidepoint(event.pos):
                active_field = "username"
            elif password_field.collidepoint(event.pos):
                active_field = "password"
            elif submit_button.collidepoint(event.pos):
                attempt_login()

        elif screen == "login" and event.type == pygame.TEXTINPUT:
            if active_field == "username" and len(username) < MAX_CREDENTIAL_LENGTH:
                username += event.text[:MAX_CREDENTIAL_LENGTH - len(username)]
            elif active_field == "password" and len(password) < MAX_CREDENTIAL_LENGTH:
                password += event.text[:MAX_CREDENTIAL_LENGTH - len(password)]

        elif screen == "login" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if active_field == "username":
                    username = username[:-1]
                else:
                    password = password[:-1]
            elif event.key == pygame.K_TAB:
                active_field = "password" if active_field == "username" else "username"
            elif event.key == pygame.K_RETURN:
                attempt_login()
        elif screen == "settings" and event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                screen = "home"

        elif screen == "session_select" and event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                screen = "home"
            elif host_game_button.collidepoint(event.pos):
                screen = "game"
            elif join_session_button.collidepoint(event.pos):
                screen = "session"

        elif screen == "session" and event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                screen = "session_select"

            for btn in session_buttons:
                if btn.is_clicked(event.pos):
                    selected_session = btn.label
                    print("Joining:", selected_session)
                    screen = "game"

        elif screen == "game" and event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if selected_piece is None:
                for piece in all_pieces:
                    if piece.rect.collidepoint((x,y)):
                        selected_piece = piece
                        break
            else:
                col = int((x - board_x) // SQUARE_SIZE)
                row = int((y - board_y) // SQUARE_SIZE)

                selected_piece.move(row, col)
                selected_piece = None


    gameDisplay.blit(bg, (0, 0))
    if screen == "login":
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
            draw_centered_text(status_message, status_font, BLACK_COLOR, submit_button.bottom + 18)
    elif screen == "settings":
        draw_centered_text( "Settings", title_font, BLACK_COLOR, HEIGHT // 2 - 200)
        draw_button(back_button, "Back")
    elif screen == "session_select":
        gameDisplay.blit(bg, (0, 0))
        draw_centered_text("Start a Match", title_font, BLACK_COLOR, HEIGHT // 2 - 200)
        session_load_screen(gameDisplay, title_font, ui_font)
        draw_button(back_button, "Back")
    elif screen == "session":
        gameDisplay.blit(bg, (0, 0))

        draw_centered_text("Join a Game Session", title_font, BLACK_COLOR, HEIGHT // 2 - 200)

        for btn in session_buttons:
            btn.draw(gameDisplay, ui_font, TAN_COLOR, BLACK_COLOR, BLACK_COLOR)

        draw_button(back_button, "Back")

    else:
        gameDisplay.blit(BOARD, (board_x, board_y))
        red_piece_set.draw(gameDisplay)
        black_piece_set.draw(gameDisplay)
        


    # Update display
    pygame.display.flip()


pygame.quit()