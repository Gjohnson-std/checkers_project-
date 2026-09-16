import pygame
import pandas as pd
import customtkinter as tk

# 1. Initialize Pygame
pygame.init()

# 2. Define window dimensions and create the gameDisplay surface
WIDTH, HEIGHT = 800, 600  # Change these numbers to match your desired window size
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")

# 3. Load the background image (using correct raw string syntax)
bg_path = r"C:\Users\Kyle Bailey\Downloads\checkers_project-\Assets\natural-wood-texture-background-surface-of-teak-wooden-desk-texture-free-photo.jpg"
bg = pygame.image.load(bg_path)

# Optional: Resize the background image to fit your window exactly
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# --- GAME LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 4. Draw the background surface
    gameDisplay.blit(bg, (0, 0))

    # (Draw rest of items/pieces here)

    # 5. Refresh the screen to actually show the updates
    pygame.display.flip()

pygame.quit()
