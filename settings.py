import pygame
from config import HEIGHT, WIDTH, button_click_sound, checker_piece_sound


class Settings:
    """Sounds and music for the game"""
    def __init__(self):
        self.sound = True
        self.music = True

        self.sound_volume = 1.0
        self.music_volume = 1.0

        self.settings_panel = pygame.rect.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 250, 400, 500)
        self.exit_settings = pygame.rect.Rect(self.settings_panel.centerx - 150, self.settings_panel.y + 400, 300, 60)

        self.sound_up = pygame.rect.Rect(self.settings_panel.centerx - 180, self.settings_panel.y + 150, 60, 60)
        self.sound_button = pygame.rect.Rect(self.settings_panel.centerx - 100, self.settings_panel.y + 150, 200, 60)
        self.sound_down = pygame.rect.Rect(self.settings_panel.centerx + 120, self.settings_panel.y + 150, 60, 60)

        self.music_up = pygame.rect.Rect(self.settings_panel.centerx - 180, self.settings_panel.y + 300, 60, 60)
        self.music_button = pygame.rect.Rect(self.settings_panel.centerx - 100, self.settings_panel.y + 300, 200, 60)
        self.music_down = pygame.rect.Rect(self.settings_panel.centerx + 120, self.settings_panel.y + 300, 60, 60)

    def play_button_sound(self):
        if self.sound:
            button_click_sound.play()

    def play_checker_piece_sound(self):
        if self.sound:
            checker_piece_sound.play()

settings = Settings()