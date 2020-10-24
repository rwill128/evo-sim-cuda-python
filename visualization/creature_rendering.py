from typing import Callable

import numpy as np


def detect_occluded_squares(g: np.ndarray, l: np.ndarray, cid: float):
    x0, y0, x1, y1 = l

    g[int(np.round(x0)), int(np.round(y0))] = cid

    slope = (y1 - y0) / (x1 - x0)

    length_of_line = np.linalg.norm((y1 - y0, x1 - x0))
    step_size = 1 / length_of_line

    x_step_size = step_size
    y_step_size = step_size * slope

    i, j = x_step_size, y_step_size

    going_right = x0 < x1
    going_left = x0 > x1
    going_up = y0 < y1
    going_down = y0 > y1

    if going_left:
        i = -i
        x_step_size = -x_step_size
        j = -j
        y_step_size = -y_step_size

    still_room_right: Callable[[float, float, float], bool] = lambda x, x2, inc: (x + inc <= x2)
    still_room_left: Callable[[float, float, float], bool] = lambda x, x2, inc: (x + inc >= x2)
    still_room_up: Callable[[float, float, float], bool] = lambda y, y2, inc: (y + inc <= y2)
    still_room_down: Callable[[float, float, float], bool] = lambda y, y2, inc: (y + inc >= y2)

    while (going_right and still_room_right(x0, x1, i) or (going_left and still_room_left(x0, x1, i))) \
            and (going_up and still_room_up(y0, y1, j) or (going_down and still_room_down(y0, y1, j))):
        g[int(np.round(x0 + i)), int(np.round(y0 + j))] = cid
        i += x_step_size
        j += y_step_size


def place_creature(t, c):
    c_id = c[0, 0]
    for l in c[1:]:
        segment_id = l[0]
        detect_occluded_squares(t, l[1:], c_id + segment_id)
