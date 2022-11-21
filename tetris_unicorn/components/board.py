from django_unicorn.components import UnicornView

from tetris_htmx import tetris


class BoardView(UnicornView):
    game_state: tetris.GameState = None
    range_board_height = range(tetris.BOARD_HEIGHT)
    range_board_width = range(tetris.BOARD_WIDTH)

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.game_state = tetris.GameState.new_game()

    def get_updates(self):
        self.game_state = tetris.get_game_state(input_=None)

    def new_game(self):
        self.game_state = tetris.GameState.new_game()

    def input(self, direction=None):
        print("Input")
        if direction not in ['left', 'right', 'up', 'down']:
            print(f"Unknown input {direction}")
        self.game_state = tetris.get_game_state(input_=direction)

    class Meta:
        javascript_exclude = ("game_state", "range_board_height", "range_board_width")
