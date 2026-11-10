import pygame
import socket
from navigate import go_to
from config import (
    BLACK_COLOR,
    HEIGHT,
    WIDTH,
    back_button,
    field_font,
    status_font,
    title_font,
)
from network import Network

# Retained for compatibility with the existing session-button tests.
session_ID = ["Session A", "Session B", "Session C"]
network = Network()
local_side = None
status_message = ""
host_ip = ""
connecting = False
ip_field = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 20, 400, 56)


def _get_lan_ip():
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("8.8.8.8", 80))
        return probe.getsockname()[0]
    except OSError:
        return "Find your IPv4 address with ipconfig"
    finally:
        probe.close()


def start_host():
    global local_side, status_message, connecting
    network.close()
    connecting = False
    try:
        network.host()
    except OSError as error:
        status_message = f"Could not host: {error}"
        return False
    local_side = "Red"
    status_message = f"Waiting for opponent at {_get_lan_ip()}:5555"
    return True


def start_join():
    global host_ip, local_side, status_message, connecting
    network.close()
    host_ip = ""
    local_side = "Black"
    connecting = False
    status_message = "Enter the host's LAN IP address."
    go_to("sessions")
    pygame.key.start_text_input()


def join_host():
    global status_message, connecting
    if connecting:
        return
    address = host_ip.strip()
    if not address:
        status_message = "Enter the host's LAN IP address."
        return
    network.join(address)
    connecting = True
    status_message = f"Connecting to {address}:5555..."

#making buttons for each joinable session
class SessionButton:
    def __init__(self, rect, label):
        self.rect = rect
        self.label = label

    def draw(self, surface, font, bg_color, border_color, text_color):
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=8)

        text_surf = font.render(self.label, True, text_color)
        surface.blit(
            text_surf,
            (self.rect.centerx - text_surf.get_width() // 2,
             self.rect.centery - text_surf.get_height() // 2)
        )

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

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
# Session screen
# --------------------------------------------------

def handle_session(event):
    global host_ip, status_message, local_side, connecting

    if event.type == pygame.TEXTINPUT:
        if len(host_ip) + len(event.text) <= 253:
            host_ip += event.text
        return

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            host_ip = host_ip[:-1]
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            join_host()
        return

    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    if back_button.collidepoint(event.pos):
        network.close()
        local_side = None
        connecting = False
        status_message = ""
        host_ip = ""
        pygame.key.stop_text_input()
        go_to("select_session")
        return

    if ip_field.collidepoint(event.pos):
        pygame.key.start_text_input()


def draw_session(surface):
    title = title_font.render("Join a LAN Game", True, BLACK_COLOR)
    surface.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 130)))

    pygame.draw.rect(surface, (255, 255, 255), ip_field, border_radius=6)
    pygame.draw.rect(surface, BLACK_COLOR, ip_field, 2, border_radius=6)
    shown_ip = host_ip or "Host IP address"
    color = BLACK_COLOR if host_ip else (110, 110, 110)
    rendered_ip = field_font.render(shown_ip, True, color)
    surface.blit(
        rendered_ip,
        (ip_field.x + 12, ip_field.centery - rendered_ip.get_height() // 2),
    )
    draw_hint = status_font.render("Press Enter to connect", True, BLACK_COLOR)
    surface.blit(draw_hint, draw_hint.get_rect(center=(WIDTH // 2, ip_field.bottom + 35)))
    status = status_font.render(status_message, True, BLACK_COLOR)
    surface.blit(status, status.get_rect(center=(WIDTH // 2, ip_field.bottom + 75)))
    pygame.draw.rect(surface, (220, 220, 220), back_button, border_radius=8)
    pygame.draw.rect(surface, BLACK_COLOR, back_button, 2, border_radius=8)
    back_text = status_font.render("Back", True, BLACK_COLOR)
    surface.blit(back_text, back_text.get_rect(center=back_button.center))


def set_network_status(message):
    global status_message
    status_message = message


def set_connecting(value):
    global connecting
    connecting = value
