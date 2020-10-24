import numpy as np


def detect_occluded_squares(g, l: np.ndarray, cid):
    x0, y0, x1, y1 = l

    slope = (y1 - y0) / (x1 - x0)

    length_of_line = np.linalg.norm((y1 - y0, x1 - x0))
    step_size = 1 / length_of_line

    i = step_size
    j = step_size * slope

    while x0 + i < x1 and y0 + j < y1:
        g[int(np.round(x0 + i)), int(np.round(y0 + j))] = cid
        i += step_size
        j += step_size * slope

