import pygame
from config import WIDTH, HEIGHT, back_button
from navigate import go_to
import navigate
from credential_store import save_credentials, MAX_CREDENTIAL_LENGTH

## --------------------------------------------------
# Login screen 
## --------------------------------------------------

# field creation 
username_field = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 90, 500, 58)
password_field = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 + 4, 500, 58)
submit_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 115, 220, 58)

# field name -> rect, used for click detection and drawing
LOGIN_FIELDS = {
    "username": username_field,
    "password": password_field,
}

# this method allows for the next page to be displayed after the login is successful
def attempt_login():
    if not navigate.username or not navigate.password:
        navigate.status_message = "Enter both a username and password."
        return

    try:
        save_credentials(navigate.username, navigate.password)
    except (OSError, ValueError, UnicodeDecodeError) as error:
        navigate.status_message = f"Could not save login: {error}"
        return

    navigate.status_message = "Login saved."
    go_to("select_session")

# --------------------------------------------------
# Login screen
# --------------------------------------------------

def login_click(event):
    if back_button.collidepoint(event.pos):
        go_to("home")
        return

    if submit_button.collidepoint(event.pos):
        attempt_login()
        return

    for field_name, field_rect in LOGIN_FIELDS.items():
        if field_rect.collidepoint(event.pos):
            navigate.active_field = field_name


def login_text(event):
    if navigate.active_field == "username":
        remaining = MAX_CREDENTIAL_LENGTH - len(navigate.username)
        navigate.username += event.text[:remaining]

    if navigate.active_field == "password":
        remaining = MAX_CREDENTIAL_LENGTH - len(navigate.password)
        navigate.password += event.text[:remaining]


def login_backspace():
    if navigate.active_field == "username":
        navigate.username = navigate.username[:-1]

    if navigate.active_field == "password":
        navigate.password = navigate.password[:-1]


def login_switch_field():
    navigate.active_field = (
        "password" if navigate.active_field == "username" else "username"
    )


    
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