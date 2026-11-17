import pygame 

screen = "home"
username = ""
password = ""
active_field = "username"
status_message = ""
selected_session = None
selected_piece = None

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
