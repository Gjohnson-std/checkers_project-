import pygame

#each session ID will be shown to the player trying to join
session_ID = ["Session A", "Session B", "Session B"]

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



    

