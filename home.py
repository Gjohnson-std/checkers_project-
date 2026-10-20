from pathlib import Path
import pygame

WIDTH = 1920
HEIGHT = 1080

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "Assets"
clock = pygame.time.Clock()

def run_home_screen(gameDisplay):
    # Load assets
    title_bg = pygame.image.load(ASSETS_DIR / "titlebg.png").convert()
    title_bg = pygame.transform.scale(title_bg, (WIDTH, HEIGHT))

    title_img = pygame.image.load(ASSETS_DIR / "title.png").convert_alpha()
    title_img = pygame.transform.scale(title_img, (700, 350))

    login_img = pygame.image.load(ASSETS_DIR / "login.png").convert_alpha()
    login_img = pygame.transform.scale(login_img, (320, 140))

    settings_img = pygame.image.load(ASSETS_DIR / "settings.png").convert_alpha()
    settings_img = pygame.transform.scale(settings_img, (320, 140))

    exit_img = pygame.image.load(ASSETS_DIR / "exit.png").convert_alpha()
    exit_img = pygame.transform.scale(exit_img, (320, 140))

    # Positioning
    title_rect = title_img.get_rect(center=(WIDTH // 2, 220))
    login_rect = login_img.get_rect(center=(WIDTH // 2, 520))
    settings_rect = settings_img.get_rect(center=(WIDTH // 2, 700))
    exit_rect = exit_img.get_rect(center=(WIDTH // 2, 880))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_rect.collidepoint(event.pos):
                    return "login"
                elif settings_rect.collidepoint(event.pos):
                    return "settings"
                elif exit_rect.collidepoint(event.pos):
                    return "exit"
                
        gameDisplay.blit(title_bg, (0, 0))
        gameDisplay.blit(title_img, title_rect)
        gameDisplay.blit(login_img, login_rect)
        gameDisplay.blit(settings_img, settings_rect)
        gameDisplay.blit(exit_img, exit_rect)
        pygame.display.flip()
        clock.tick(60)