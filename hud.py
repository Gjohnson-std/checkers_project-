import pygame
from config import WIDTH, HEIGHT, ASSETS_DIR
from board import red_piece, red_king, black_piece, black_king
import sessions

# --------------------------------------------------
# HUD aspect ratio and loading 
# --------------------------------------------------

class HUD:
    def __init__(self):
        # Loading hud while preserving the aspect ratio
        image_path = ASSETS_DIR / "HUD.png"
        starter_image = pygame.image.load(image_path).convert_alpha()
        starter_width, starter_height = starter_image.get_size()
        scale = min(
            WIDTH / starter_width,
            HEIGHT / starter_height
        )
        new_width = int(starter_width * scale)
        new_height = int(starter_height * scale)
        self.frame = pygame.transform.smoothscale(
            starter_image,
            (new_width, new_height)
        )
        # Centering HUD using self 
        self.x = (WIDTH - new_width) // 2
        self.y = (HEIGHT - new_height) // 2
        # Font for piece counts
        self.count_font = pygame.font.Font(None, 30)
        # Sprites for the icons next to font text
        self.piece_sprites = {
            "red": red_piece,
            "red_king": red_king,
            "black": black_piece,
            "black_king": black_king
        }
        self.scale = scale
# --------------------------------------------------
# Timers for each player under init
# --------------------------------------------------
        self.time_limit = 5 * 60 # 5 mins in seconds
        self.player_times = {
            "Red": self.time_limit,
            "Black": self.time_limit
        }
        self.last_timer_update = pygame.time.get_ticks()
        self.active_timer = "Red"
        self.timer_started = False

    def draw(self, surface, board_state):
        surface.blit(self.frame, (self.x, self.y))
        self.updateTimer(board_state)
        counts = self.pieceCounts(board_state)
        self.drawPieceCounts(surface, counts)
        self.drawCapturedPieces(surface, board_state)
        self.drawTurn(surface, board_state)
        self.drawTimer(surface)

# --------------------------------------------------
# Displaying Captured Pieces (left and right)
# --------------------------------------------------

# Method to get the Captured pieces in the current game based on color
    def getCapturedPieces(self, board_state):
        """Separates captured pieces based on the original color / king status"""
        captured = {
            "Red": [],
            "Black": []
        }
        for piece in board_state.captured_pieces:
            captured[piece.color].append(piece)
        return captured
    def drawCapturedPieces(self, surface, board_state):
        captured = self.getCapturedPieces(board_state)
        local_player = sessions.local_side
        opponent = "Black" if local_player == "Red" else "Red"
        # Left = pieces captured by local player
        # Right = pieces captured by opponent 

        left_pieces = captured[opponent]
        right_pieces = captured[local_player]
        icon_size = int(30 * self.scale)
        spacing = int(35 * self.scale)
        # Display captured pieces on left
        for index, piece in enumerate(left_pieces):
            key = piece.color.lower()
            if piece.king:
                key += "_king"
            sprite = pygame.transform.smoothscale(
                self.piece_sprites[key],
                (icon_size, icon_size)
            )
            x = self.x + int(100 * self.scale) + index * spacing
            y = self.y + int(450 * self.scale)
            surface.blit(sprite, (x, y))
        # Display captured pieces on right 
        for index, piece in enumerate(right_pieces):
            key = piece.color.lower()
            if piece.king:
                key += "_king"
            sprite = pygame.transform.smoothscale(
                self.piece_sprites[key],
                (icon_size, icon_size)
            )
            x = self.x + int(1200 * self.scale) + index * spacing
            y = self.y + int(450 * self.scale)
            surface.blit(sprite, (x, y))
# --------------------------------------------------
# Live Piece Counts Logic
# --------------------------------------------------
    def pieceCounts(self, board_state):
        red_pieces = board_state.get_remaining_pieces("Red")
        black_pieces = board_state.get_remaining_pieces("Black")
        counts = {
            "red": sum(not piece.king for piece in red_pieces),
            "red_king": sum(piece.king for piece in red_pieces),
            "black": sum(not piece.king for piece in black_pieces),
            "black_king": sum(piece.king for piece in black_pieces)
        }
        return counts 
# --------------------------------------------------
# Displaying Live Piece Counts 
# --------------------------------------------------
    def drawPieceCounts(self, surface, counts):
        loc_pos = [
            ("red", 405, 920),
            ("red_king", 650, 920),
            ("black", 890, 920),
            ("black_king", 1135, 920)
        ]
# Getting sprites and resizing to fit in boxes
        for key, x, y in loc_pos:
            sprite = self.piece_sprites[key]
            icon_size = int(36 * self.scale)
            icon = pygame.transform.smoothscale(sprite, (icon_size, icon_size))
# Position sprites relative to HUD and make font white
            pos_x = self.x + int(x * self.scale)
            pos_y = self.y + int(y * self.scale)
            count_text = self.count_font.render(str(counts[key]), True, (255,255,255))
            text_x = pos_x + icon_size + 5
            text_y = pos_y + (icon_size - count_text.get_height()) // 2
# Drawing the checker sprites + count
            surface.blit(icon, (pos_x, pos_y))
            surface.blit(count_text, (text_x, text_y))
# --------------------------------------------------
# Turn Logic
# --------------------------------------------------
    def drawTurn(self, surface, board_state):
        current_player = board_state.current_player
        if current_player == "Red":
            sprite = self.piece_sprites["red"]
            turn_text = "RED"
        else:
            sprite = self.piece_sprites["black"]
            turn_text = "BLACK"
        # Resizing sprite to fit in box and turn text rendering
        icon_size = int(36 * self.scale)
        icon = pygame.transform.smoothscale(sprite, (icon_size, icon_size))
        text = self.count_font.render(turn_text, True, (255,255,255))
        center_x = self.x + int(705 * self.scale)
        center_y = self.y + int(65 * self.scale)
        total_width = icon_size + 8 + text.get_width()
        pos_x = center_x - total_width // 2
        pos_y = center_y - icon_size // 2
        text_x = pos_x + icon_size + 8
        text_y = center_y - text.get_height() // 2
        # Drawing sprite and the turn text
        surface.blit(icon, (pos_x, pos_y))
        surface.blit(text, (text_x, text_y))
# --------------------------------------------------
# Timer Logic
# --------------------------------------------------
    def updateTimer(self, board_state):
        if not self.timer_started:
            return
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_timer_update) / 1000
        current_player = board_state.current_player
        self.player_times[self.active_timer] = max(
            0,
            self.player_times[self.active_timer] - elapsed
        )
        # Switch current player timer
        self.active_timer = current_player
        self.last_timer_update = current_time

# Timer will only start once opponent joins 
    def startTimer(self, board_state):
        self.timer_started = True
        self.active_timer = board_state.current_player
        self.last_timer_update = pygame.time.get_ticks()

# --------------------------------------------------
# Displaying the Timer
# --------------------------------------------------
    def drawTimer(self, surface):
        remaining = int(self.player_times[self.active_timer])
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text = f"{minutes}:{seconds:02d}"
        text = self.count_font.render(timer_text, True, (255,255,255))
        center_x = self.x + int(1050 * self.scale)
        center_y = self.y + int(100 * self.scale)
        text_x = center_x - text.get_width() // 2
        text_y = center_y - text.get_height() // 2
        surface.blit(text, (text_x, text_y))