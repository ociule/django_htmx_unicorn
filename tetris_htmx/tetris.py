import math
import random
import time
from dataclasses import dataclass, field

from django.core.cache import cache

from .tetrominoes import Tetrominoes

STEP_DURATION = 1.0
BETWEEN_NEW_PIECE_STEPS = 10
BOARD_HEIGHT = 20
BOARD_WIDTH = 10


@dataclass
class GameState:
    game_start_timestamp: float
    board: list
    unsupported_pieces: list = field(default_factory=lambda: [])
    next_new_piece_step: int = 0
    next_drop: int = 1

    @classmethod
    def new_game(cls):
        gs = GameState(
            game_start_timestamp=time.time(),
            board=new_board(),
        )

        cache.set("game_state", gs)
        return gs

    @classmethod
    def get(cls):
        return cache.get("game_state", None) or GameState.new_game()

    @classmethod
    def set(cls, gs):
        return cache.set("game_state", gs)

    def should_introduce_new_piece(self):
        game_step = self.get_game_step()
        return game_step >= self.next_new_piece_step

    def should_drop(self):
        game_step = self.get_game_step()
        return game_step >= self.next_drop

    def get_game_step(self):
        seconds_since_start = time.time() - self.game_start_timestamp
        return math.floor(seconds_since_start / STEP_DURATION)

    def apply_input(self, input_):
        if input_ not in ['left', 'right', 'up', 'down']:
            print(f"Unknown input {input_}")
            return self

        movable_piece = self.unsupported_pieces[0]
        row, col, tetromino = movable_piece

        if not self.can_piece_go_direction(movable_piece, input_):
            return self

        if input_ == "down":
            move_piece_down(self, 0)
        elif input_ == "left":
            dir_row, dir_col = 0, -1
            for ix_t_row, t_row in enumerate(tetromino.footprint):
                for ix_t_col, t_col in enumerate(tetromino.footprint[ix_t_row]):
                    self.board[row + ix_t_row + dir_row][col + ix_t_col + dir_col] = tetromino.footprint[ix_t_row][
                        ix_t_col]
            # clear right col
            for ix_t_row, _ in enumerate(tetromino.footprint):
                t_col = len(tetromino.footprint[0]) - 1
                self.board[row + ix_t_row][col + t_col] = 0
            row, col = row + dir_row, col + dir_col
        elif input_ == "right":
            dir_row, dir_col = 0, +1
            for ix_t_row, t_row in enumerate(tetromino.footprint):
                for ix_t_col, t_col in enumerate(tetromino.footprint[ix_t_row]):
                    self.board[row + ix_t_row + dir_row][col + ix_t_col + dir_col] = tetromino.footprint[ix_t_row][
                        ix_t_col]
            # clear left col
            for ix_t_row, _ in enumerate(tetromino.footprint):
                t_col = 0
                self.board[row + ix_t_row][col + t_col] = 0
            row, col = row + dir_row, col + dir_col
        elif input_ == "up":  # Rotate!
            pass
        self.unsupported_pieces[0] = (row, col, tetromino)
        return self

    def can_piece_go_direction(self, piece, input_):
        row, col, tetromino = piece
        if input_ == "down":
            if row == BOARD_HEIGHT - 1:
                return False
            t_row_to_check = len(tetromino.footprint) - 1
            board_row_to_check = row + len(tetromino.footprint)
            print(t_row_to_check, board_row_to_check)
            for ix_col in range(len(tetromino.footprint[t_row_to_check])):
                if tetromino.footprint[t_row_to_check][ix_col] != 0:
                    print(f"Should check {t_row_to_check}, {ix_col}")
                    print(board_row_to_check, col + ix_col, self.board[board_row_to_check][col + ix_col])
                    if self.board[board_row_to_check][col + ix_col] != 0:
                        return False
        elif input_ == "left":
            pass
        elif input_ == "right":
            pass
        elif input_ == "up":
            pass
        return True


def move_piece_down(game_state, piece_index):
    row, col, tetromino = game_state.unsupported_pieces[piece_index]

    dir_row, dir_col = 1, 0
    for ix_t_row, t_row in enumerate(tetromino.footprint):
        for ix_t_col, t_col in enumerate(tetromino.footprint[ix_t_row]):
            game_state.board[row + ix_t_row + dir_row][col + ix_t_col + dir_col] = tetromino.footprint[ix_t_row][
                ix_t_col]
    # clear top row
    for ix_t_col, _ in enumerate(tetromino.footprint[0]):
        game_state.board[row][col + ix_t_col] = 0
    row, col = row + dir_row, col + dir_col
    game_state.unsupported_pieces[piece_index] = row, col, tetromino
    return game_state


def new_board():
    board = []
    for _ in range(BOARD_HEIGHT):
        board.append([0] * BOARD_WIDTH)
    return board


def copy_footprint(row, col, tetramino, board):
    for iy, footprint_row in enumerate(tetramino.footprint):
        for ix, footprint_col in enumerate(tetramino.footprint[iy]):
            if footprint_col != 0:
                board[row + iy][col + ix] = footprint_col
    return board


def delete_footprint(row, col, tetramino, board):
    for iy, footprint_row in enumerate(tetramino.footprint):
        for ix, footprint_col in enumerate(tetramino.footprint[iy]):
            if footprint_col != 0:
                board[row + iy][col + ix] = 0
    return board


def drop_unsupported_pieces(game_state, input_):

    # New pieces, at the top, are appended to the last place in unsupported
    # We range from bottom piece (index = 0) to top
    for ix in range(len(game_state.unsupported_pieces)):
        piece = game_state.unsupported_pieces[ix]
        if game_state.can_piece_go_direction(piece, "down"):
            game_state = move_piece_down(game_state, ix)
        else:
            # Remove from unsupported pieces
            print(f"Remove from unsupported pieces {ix} {piece}")
            game_state.unsupported_pieces.pop(ix)

    return game_state


def update_game_board(input_):
    game_state = GameState.get()

    if input_:
        game_state = game_state.apply_input(input_)


    if game_state.should_drop():
        game_state = drop_unsupported_pieces(game_state, input_)
        game_state.next_drop = game_state.get_game_step() + 1

    if game_state.should_introduce_new_piece():
        new_piece = random.choice(list(Tetrominoes))
        game_state.board = copy_footprint(0, 4, new_piece, game_state.board)

        game_state.unsupported_pieces.append((0, 4, new_piece))
        game_state.next_new_piece_step = game_state.get_game_step() + BETWEEN_NEW_PIECE_STEPS

    return game_state


def get_game_state(input_):
    game_state = update_game_board(input_)
    GameState.set(game_state)

    return game_state
