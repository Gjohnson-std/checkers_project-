import pygame

#making buttons for each joinable session
class Button:
    def __init__(self, surface, x, y, w, h, text, onClick):
        self.surface = surface
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.onClick = onClick
        self.font = pygame.font.Font(None, 40)

    def draw(self):
        pygame.draw.rect(self.surface, (200,200,200), self.rect)
        pygame.draw.rect(self.surface, (0,0,0), self.rect, 2)

        label = self.font.render(self.text, True, (0,0,0))
        self.surface.blit(label, (self.rect.x + 10, self.rect.y + 5))
        #making buttons

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.onClick()



    

