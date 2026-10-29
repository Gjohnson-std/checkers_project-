from config import load_asset, WIDTH, HEIGHT
from navigate import go_to
import pygame


# --------------------------------------------------
# Home Page UI rectangles
# --------------------------------------------------
# Home screen images (loaded once, after the display exists)
title_bg = load_asset("titlebg.png", (WIDTH, HEIGHT), alpha=False)
title_img = load_asset("Title.png", (700, 350))
login_img = load_asset("Login.png", (320, 140))
settings_img = load_asset("Settings.png", (320, 140))
exit_img = load_asset("Exit.png", (320, 140))

# Home screen button rects (positions taken from home.py)
title_rect = title_img.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.204)))
login_rect = login_img.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.481)))
settings_rect = settings_img.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.648)))
exit_rect = exit_img.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.815)))


# --------------------------------------------------
# Home screen
# --------------------------------------------------



#uses go to navaigation to go to the login screen 
def home_login():
    go_to("login")


def home_settings():
    # No settings screen yet: add "settings" to the dispatch tables later.
    print("Settings screen not implemented yet")

#closes the game when exit is clicked
def home_exit():
    pygame.event.post(pygame.event.Event(pygame.QUIT))

## --------------------------------------------------
# Home buttons 
# -------------------------------------------------

# button rect -> action
HOME_BUTTONS = (
    (login_rect, home_login),
    (settings_rect, home_settings),
    (exit_rect, home_exit),
)

#handles each indivicual button click on the home screen and calls the appropriate function
def handle_home(event):
    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    for rect, action in HOME_BUTTONS:
        if rect.collidepoint(event.pos):
            action()
            return