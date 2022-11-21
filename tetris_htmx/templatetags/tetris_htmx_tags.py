from django import template

register = template.Library()

PIECE_INT_TO_COLOR = {
    0: "dark",
    1: "danger",
    2: "primary",
    3: "success",
    4: "warning",
    5: "info",
    6: "secondary",
    7: "light",
}


@register.simple_tag
def grid_color(board, row, column):
    piece_type = board[row][column]
    return PIECE_INT_TO_COLOR[piece_type]
