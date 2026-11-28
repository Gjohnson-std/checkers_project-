import pygame
from config import HEIGHT, WIDTH, button_click_sound, checker_piece_sound
import navigate


class Settings:
    """Sounds and music for the game"""
    def __init__(self):
        self.sound = True
        self.music = True

        self.sound_volume = 1.0
        self.music_volume = 1.0
        self.visible = False

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
            button_click_sound.set_volume(self.sound_volume)
            button_click_sound.play()

    def play_checker_piece_sound(self):
        if self.sound:
            checker_piece_sound.set_volume(self.sound_volume)
            checker_piece_sound.play()

settings = Settings()

def handle_settings(event):
    """coontrol sound and muisc volume"""
    if event.type != pygame.MOUSEBUTTONDOWN:
        return
    if settings.sound_up.collidepoint(event.pos):
        settings.play_button_sound()
        settings.sound_volume = min(settings.sound_volume + 0.1, 1.0)
    elif settings.sound_button.collidepoint(event.pos):
        settings.play_button_sound()
        settings.sound = not settings.sound
    elif settings.sound_down.collidepoint(event.pos):
        settings.play_button_sound()
        settings.sound_volume = max(settings.sound_volume - 0.1, 0.0)
    elif settings.music_up.collidepoint(event.pos):
        settings.play_button_sound()
        settings.music_volume = min(settings.music_volume + 0.1, 1.0)
        pygame.mixer.music.set_volume(settings.music_volume)
    elif settings.music_button.collidepoint(event.pos):
        settings.play_button_sound()
        settings.music = not settings.music
        if settings.music:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
    elif settings.music_down.collidepoint(event.pos):
        settings.play_button_sound()
        settings.music_volume = max(settings.music_volume - 0.1, 0.0)
        pygame.mixer.music.set_volume(settings.music_volume)
    elif settings.exit_settings.collidepoint(event.pos):
        settings.play_button_sound()
        settings.visible = not settings.visible
