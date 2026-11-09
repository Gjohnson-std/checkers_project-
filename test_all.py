import importlib
import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pygame
import pandas as pd
import pytest

pygame.init()
pygame.display.set_mode((800, 600))

import credential_store as cs
import select_session as ss
from sessions import SessionButton, session_ID


@pytest.fixture
def fake_images(monkeypatch):
    """Blank surfaces instead of real PNGs, so no asset files are needed."""
    monkeypatch.setattr(pygame.image, "load",
                        lambda *a, **k: pygame.Surface((64, 64), pygame.SRCALPHA))


@pytest.fixture
def pieces(fake_images):
    sys.modules.pop("pieces", None)  # pieces.py loads images at import time
    return importlib.import_module("pieces")


# ---------------- credential_store ----------------

@pytest.fixture
def csv_path(tmp_path, monkeypatch):
    path = tmp_path / "users.csv"
    monkeypatch.setattr(cs, "CREDENTIALS_PATH", path)
    return path


class TestCredentials:
    def test_saves_and_appends(self, csv_path):
        cs.save_credentials("alice", "one")
        cs.save_credentials("bob", "two")
        df = pd.read_csv(csv_path, dtype=str)
        assert list(df.columns) == ["username", "password"]
        assert df["username"].tolist() == ["alice", "bob"]

    @pytest.mark.parametrize("user,pw", [("", "pw"), ("user", ""), ("u" * 17, "pw"), ("user", "p" * 17)])
    def test_rejects_bad_input(self, csv_path, user, pw):
        with pytest.raises(ValueError):
            cs.save_credentials(user, pw)
        assert not csv_path.exists()

    def test_accepts_max_length(self, csv_path):
        cs.save_credentials("u" * 16, "p" * 16)
        assert csv_path.exists()

    def test_rejects_malformed_csv(self, csv_path):
        csv_path.write_text("name,pass\nx,y\n")
        with pytest.raises(ValueError):
            cs.save_credentials("alice", "pw")


# ---------------- sessions ----------------

class TestSessions:
    def test_session_ids_exist_and_unique(self):
        assert session_ID and len(set(session_ID)) == len(session_ID)

    def test_button_click_detection(self):
        btn = SessionButton(pygame.Rect(100, 100, 300, 50), "Session A")
        assert btn.is_clicked((250, 125))
        assert not btn.is_clicked((50, 50))


# ---------------- select_session ----------------

class TestSelectSession:
    def test_buttons_dont_overlap_and_fit_screen(self):
        screen = pygame.Rect(0, 0, ss.WIDTH, ss.HEIGHT)
        assert not ss.host_game_button.colliderect(ss.join_session_button)
        assert screen.contains(ss.host_game_button)
        assert screen.contains(ss.join_session_button)

    def test_click_routing(self):
        def click(pos):
            return pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1)
        assert ss.handle_session_click(click(ss.host_game_button.center)) == "game"
        assert ss.handle_session_click(click((0, 0))) == "session"

    def test_screen_draws_without_error(self):
        font = pygame.font.Font(None, 25)
        ss.session_load_screen(pygame.Surface((800, 600)), font, font)


# ---------------- pieces ----------------

class TestBoardState:
    def test_grid_tracks_piece_moves(self):
        import board

        pieces = board.create_all_pieces()
        state = board.BoardState(pieces)
        piece = state.cells[2][1]

        assert len(state.cells) == 8
        assert all(len(row) == 8 for row in state.cells)
        assert sum(cell is not None for row in state.cells for cell in row) == 24
        assert not state.move_piece(None, 3, 0)  # no piece on the starting square
        assert not state.move_piece(piece, 2, 0)  # horizontal move
        assert not state.move_piece(piece, 3, 1)  # vertical move
        assert not state.move_piece(piece, 4, 3)  # more than one square
        assert state.current_player == "Red"
        assert not state.move_piece(state.cells[5][0], 4, 1)  # Black moves second

        assert state.move_piece(piece, 3, 0)
        assert state.current_player == "Black"
        assert state.cells[2][1] is None
        assert state.cells[3][0] is piece
        assert (piece.row, piece.col) == (3, 0)

        black_piece = state.cells[5][0]
        assert state.move_piece(black_piece, 4, 1)
        assert state.current_player == "Red"

        piece.king = True
        assert state.move_piece(piece, 2, 1)
        assert state.current_player == "Black"
        assert state.cells[3][0] is None
        assert state.cells[2][1] is piece

    def test_jump_captures_opponent(self):
        import board

        image = pygame.Surface((40, 40))
        red_piece = board.CheckerPiece("", image, image, 0, 0, 3, 2, 46.875)
        red_piece.set_pieceID(0, "Red")
        black_piece = board.CheckerPiece("", image, image, 0, 0, 4, 3, 46.875)
        black_piece.set_pieceID(0, "Black")
        pieces = pygame.sprite.Group(red_piece, black_piece)
        state = board.BoardState(pieces)

        assert state.move_piece(red_piece, 5, 4)
        assert state.cells[3][2] is None
        assert state.cells[4][3] is None
        assert state.cells[5][4] is red_piece
        assert black_piece not in pieces
        assert state.current_player == "Black"

    def test_cannot_jump_own_piece(self):
        import board

        image = pygame.Surface((40, 40))
        red_piece = board.CheckerPiece("", image, image, 0, 0, 3, 2, 46.875)
        red_piece.set_pieceID(0, "Red")
        other_red_piece = board.CheckerPiece("", image, image, 0, 0, 4, 3, 46.875)
        other_red_piece.set_pieceID(1, "Red")
        state = board.BoardState(pygame.sprite.Group(red_piece, other_red_piece))

        assert not state.move_piece(red_piece, 5, 4)
        assert state.cells[3][2] is red_piece
        assert state.cells[4][3] is other_red_piece

    def test_multiple_jumps_keep_piece_forced_until_chain_ends(self):
        import board

        image = pygame.Surface((40, 40))
        red_piece = board.CheckerPiece("", image, image, 0, 0, 1, 0, 46.875)
        red_piece.set_pieceID(0, "Red")
        black_piece_one = board.CheckerPiece("", image, image, 0, 0, 2, 1, 46.875)
        black_piece_one.set_pieceID(0, "Black")
        black_piece_two = board.CheckerPiece("", image, image, 0, 0, 4, 3, 46.875)
        black_piece_two.set_pieceID(1, "Black")
        other_red_piece = board.CheckerPiece("", image, image, 0, 0, 1, 6, 46.875)
        other_red_piece.set_pieceID(1, "Red")
        pieces = pygame.sprite.Group(
            red_piece, black_piece_one, black_piece_two, other_red_piece
        )
        state = board.BoardState(pieces)

        assert state.move_piece(red_piece, 3, 2)
        assert state.must_continue_piece is red_piece
        assert state.current_player == "Red"
        assert not state.move_piece(other_red_piece, 2, 5)
        # The same piece captures again, then the turn passes to Black.
        assert state.move_piece(red_piece, 5, 4)
        assert state.must_continue_piece is None
        assert state.current_player == "Black"
        assert black_piece_one not in pieces and black_piece_two not in pieces


class TestPieces:
    def test_move_and_king(self, pieces):
        img = pygame.Surface((40, 40))
        p = pieces.CheckerPiece("", img, pygame.Surface((40, 40)), 100, 50, 2, 3, 46.875)
        p.move(5, 6)
        assert (p.row, p.col) == (5, 6)
        p.king_me()
        assert p.king and p.image is p.king_piece_img

    def test_starting_layout(self, pieces):
        red = pieces.create_red_pieces(pieces.red_piece, 0, 0)
        black = pieces.create_black_pieces(pieces.black_piece, 0, 0)
        assert len(red) == 12 and len(black) == 12
        assert {p.row for p in red} == {0, 1, 2}
        assert {p.row for p in black} == {5, 6, 7}
        squares = [(p.row, p.col) for p in list(red) + list(black)]
        assert len(set(squares)) == 24                      # no overlaps
        assert all((r + c) % 2 == 1 for r, c in squares)    # dark squares only


# ---------------- home ----------------

class TestHome:
    @pytest.mark.parametrize("y,expected", [(520, "login"), (700, "settings"), (880, "exit")])
    def test_home_buttons(self, fake_images, y, expected):
        import home
        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(home.WIDTH // 2, y), button=1))
        assert home.run_home_screen(pygame.Surface((home.WIDTH, home.HEIGHT))) == expected
