from django.shortcuts import render

from tetris_htmx.templatetags.tetris_htmx_tags import grid_color


def index(request):
    return render(request, "index_unicorn.html", {"grid_color": grid_color})
