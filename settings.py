import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from config import HEIGHT, WIDTH, bg


class Settings:
    def __init__(self):
        self.sound_volume = 50
        self.music_volume = 50
        self.sound = True
        self.music = True
        self.timer = True 
        self.panel_rect = pygame.Rect((WIDTH-500)//2, (HEIGHT-500)//2, 500, 500)

        self.sound_up = pygame.Rect(WIDTH//2-150, 250, 80, 60)
        self.sound_down = pygame.Rect(WIDTH//2-250, 250, 80, 60)
        self.sound_off = pygame.Rect(WIDTH//2-350, 250, 80, 60)

        self.music_up = pygame.Rect(WIDTH//2-150, 400, 80, 60)
        self.music_down = pygame.Rect(WIDTH//2-250, 400, 80, 60)
        self.music_off = pygame.Rect(WIDTH//2-350, 400, 80, 60)

        self.sound_button = pygame.Rect(self.panel_rect.centerx - 150, self.panel_rect.y+200, 300, 60)
        self.music_button = pygame.Rect(self.panel_rect.centerx - 150, self.panel_rect.y+300, 300, 60)
        self.exit_settings = pygame.Rect(self.panel_rect.centerx - 150, self.panel_rect.y+400, 300, 60)













        
