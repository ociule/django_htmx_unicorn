from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import tetris_htmx.tetris as tetris


def index(request):
    if request.method == 'POST' and request.htmx:
        input = request.htmx.trigger_name
    else:
        input = None

    if request.htmx:
        template_name = "play_area.html"
    else:
        template_name = "index.html"

    game_state = tetris.get_game_state(input)

    context = {"range_board_width": range(tetris.BOARD_WIDTH), "range_board_height": range(tetris.BOARD_HEIGHT), 'game_state': game_state}
    return render(request, template_name, context=context)
