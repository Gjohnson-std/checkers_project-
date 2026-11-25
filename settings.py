import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from config import HEIGHT, WIDTH, bg, button_sound, piece_move_sound


class Settings:
    def __init__(self):
        """Controls the game music and sound affects"""
        self.sound = True
        self.music = True
        self.timer = True 

        self.sound_volume = 0.5
        self.music_volume = 0.5

        self.panel_rect = pygame.Rect((WIDTH-500)//2, (HEIGHT-500)//2, 500, 500)

        self.sound_button = pygame.Rect(self.panel_rect.centerx - 150, self.panel_rect.y+200, 300, 60)
        self.music_button = pygame.Rect(self.panel_rect.centerx - 150, self.panel_rect.y+300, 300, 60)
        self.exit_settings = pygame.Rect(self.panel_rect.centerx - 150, self.panel_rect.y+400, 300, 60)

    def play_button(self):
        """plays button click sound"""
        if self.sound:
            button_sound.play()

    def play_piece_move_sound(self):
        """plays piece movement sound"""
        if self.sound:
            piece_move_sound.play()

settings = Settings()













        
