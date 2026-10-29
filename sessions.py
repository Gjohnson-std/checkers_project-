import pygame
from navigate import go_to
import navigate
from config import HEIGHT, WIDTH, back_button

#each session ID will be shown to the player trying to join
session_ID = ["Session A", "Session B", "Session C"]

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

    if event.type != pygame.MOUSEBUTTONDOWN:
        return

    if back_button.collidepoint(event.pos):
        go_to("select_session")
        return

    for btn in session_buttons:
        if btn.is_clicked(event.pos):
            navigate.selected_session = btn.label
            print("Joining:", navigate.selected_session)
            go_to("game")
            return



    

