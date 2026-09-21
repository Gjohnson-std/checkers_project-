import pygame
import pandas as pd

pygame.init()

WIDTH, HEIGHT = 800, 600  # Change these numbers to match window size
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")

bg_path = r"Assets\bg.jpg"  # Change this to the path of your background image
bg = pygame.image.load(bg_path)

bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# --- GAME LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    gameDisplay.blit(bg, (0, 0))


    pygame.display.flip()

pygame.quit()
