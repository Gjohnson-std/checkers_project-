import pygame


# --------------------------------------------------
# Screen Settings
# --------------------------------------------------

WIDTH = 800
HEIGHT = 600

BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
BUTTON_COLOR = (220, 220, 220)


# --------------------------------------------------
# Session Buttons | Host and Join
# --------------------------------------------------

host_game_button = pygame.Rect(
    WIDTH // 2 - 180,
    HEIGHT // 2,
    360,
    64
)

join_session_button = pygame.Rect(
    WIDTH // 2 - 180,
    HEIGHT // 2 + 75,
    360,
    64
)


# --------------------------------------------------
# Draw Button
# --------------------------------------------------

def draw_button(surface, button, text, font):

    pygame.draw.rect(
        surface,
        BUTTON_COLOR,
        button,
        border_radius=8
    )

    pygame.draw.rect(
        surface,
        BLACK_COLOR,
        button,
        3,
        border_radius=8
    )

    text_surface = font.render(
        text,
        True,
        BLACK_COLOR
    )

    text_rect = text_surface.get_rect(
        center=button.center
    )

    surface.blit(
        text_surface,
        text_rect
    )


# --------------------------------------------------
# Session Screen
# --------------------------------------------------

def session_load_screen(surface, title_font, button_font):

    # Page title
    title = title_font.render(
        "Start a Match",
        True,
        BLACK_COLOR
    )

    title_rect = title.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 100)
    )

    surface.blit(
        title,
        title_rect
    )

    # Host button
    draw_button(
        surface,
        host_game_button,
        "Host Game",
        button_font
    )

    # Join button
    draw_button(
        surface,
        join_session_button,
        "Join a Session",
        button_font
    )


# --------------------------------------------------
# Session Clicks
# --------------------------------------------------

def handle_session_click(event):

    if host_game_button.collidepoint(event.pos):
        return "game"

    elif join_session_button.collidepoint(event.pos):
        return "game"

    return "session"