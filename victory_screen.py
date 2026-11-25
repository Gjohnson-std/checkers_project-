
import pygame
import random
import math

RED = (245, 49, 53)
DARK_RED = (175, 12, 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class VictoryScreen:
    def __init__(self, screen, player_won):
        self.player_won = player_won
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.start_time = pygame.time.get_ticks()

        self.title_font = pygame.font.SysFont(
            "Arial Rounded MT Bold", 105, bold=True
        )
        self.text_font = pygame.font.SysFont(
            "Arial Rounded MT Bold", 40, bold=True
        )
        self.button_font = pygame.font.SysFont(
            "Arial Rounded MT Bold", 32, bold=True
        )

        # Capture the current game background.
        original = screen.copy()

        # Blur by shrinking and enlarging the image.
        small = pygame.transform.smoothscale(
            original,
            (max(1, self.width // 14),
             max(1, self.height // 14))
        )
        self.background = pygame.transform.smoothscale(
            small, (self.width, self.height)
        )

        # Darken the background slightly.
        shade = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        shade.fill((0, 0, 0, 105))
        self.background.blit(shade, (0, 0))

        self.confetti = []
        for _ in range(160):
            self.confetti.append({
                "x": random.uniform(0, self.width),
                "y": random.uniform(-self.height, 0),
                "speed": random.uniform(2, 6),
                "size": random.randint(5, 11),
                "color": random.choice(
                    [RED, WHITE, BLACK]
                ),
                "drift": random.uniform(-1, 1),
            })

        center_x = self.width // 2
        center_y = self.height // 2

        self.panel = pygame.Rect(
            center_x - 420, center_y - 245, 840, 490
        )

        self.yes_button = pygame.Rect(
            center_x - 315, center_y + 110, 275, 75
        )
        self.no_button = pygame.Rect(
            center_x + 40, center_y + 110, 275, 75
        )

    def outlined_text(self, text, font, center, fill):
        # Thick red outer outline.
        outer = font.render(text, True, RED)
        inner = font.render(text, True, BLACK)
        main = font.render(text, True, fill)

        rect = main.get_rect(center=center)

        for dx in range(-7, 8, 2):
            for dy in range(-7, 8, 2):
                self.screen.blit(
                    outer, rect.move(dx, dy)
                )

        for dx, dy in [
            (-3, 0), (3, 0), (0, -3), (0, 3),
            (-2, -2), (2, 2), (-2, 2), (2, -2)
        ]:
            self.screen.blit(
                inner, rect.move(dx, dy)
            )

        self.screen.blit(main, rect)

    def draw_button(self, rect, label):
        mouse = pygame.mouse.get_pos()
        hovering = rect.collidepoint(mouse)

        color = DARK_RED if hovering else RED

        pygame.draw.rect(
            self.screen, DARK_RED,
            rect.inflate(4, 4),
            border_radius=24
        )
        pygame.draw.rect(
            self.screen, color,
            rect, border_radius=22
        )

        text = self.button_font.render(
            label, True, WHITE
        )
        self.screen.blit(
            text, text.get_rect(center=rect.center)
        )

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Falling confetti.
        for piece in self.confetti:
            piece["y"] += piece["speed"]
            piece["x"] += piece["drift"]

            if piece["y"] > self.height:
                piece["y"] = -15
                piece["x"] = random.uniform(
                    0, self.width
                )

            pygame.draw.rect(
                self.screen,
                piece["color"],
                (
                    int(piece["x"]),
                    int(piece["y"]),
                    piece["size"],
                    piece["size"] // 2 + 2
                )
            )

        # White panel with red border.
        pygame.draw.rect(
            self.screen, RED,
            self.panel, border_radius=35
        )

        inner_panel = self.panel.inflate(-14, -14)
        pygame.draw.rect(
            self.screen, WHITE,
            inner_panel, border_radius=28
        )

        # Checkerboard trim.
        tile = 22
        for x in range(
            inner_panel.left + 12,
            inner_panel.right - 12,
            tile
        ):
            for row in range(2):
                color = BLACK if (
                    (x // tile + row) % 2 == 0
                ) else WHITE

                pygame.draw.rect(
                    self.screen, color,
                    (
                        x,
                        inner_panel.top + 8 + row * tile,
                        tile, tile
                    )
                )

                pygame.draw.rect(
                    self.screen, color,
                    (
                        x,
                        inner_panel.bottom - 52 + row * tile,
                        tile, tile
                    )
                )

        # Subtle title bounce.
        elapsed = (
            pygame.time.get_ticks() - self.start_time
        ) / 1000

        bounce = int(math.sin(elapsed * 3) * 5)

        self.outlined_text(
            "YOU WIN!" if self.player_won else "YOU LOSE!",
            self.title_font,
            (
                self.width // 2,
                self.height // 2 - 75 + bounce
            ),
            WHITE
        )

        question = self.text_font.render(
            "PLAY AGAIN?", True, BLACK
        )
        self.screen.blit(
            question,
            question.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 + 45
                )
            )
        )

        self.draw_button(self.yes_button, "YES")
        self.draw_button(self.no_button, "NO")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.yes_button.collidepoint(event.pos):
                    return "select_sessions"

                if self.no_button.collidepoint(event.pos):
                    return "main_menu"

        return None
