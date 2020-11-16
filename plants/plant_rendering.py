from typing import Callable

import numpy as np
import numba as nb

# TODO: This can be made simpler for plants that are using only ints of length 1. It's just a grid, or it should be
# Probably some or most of this code can be used for animals though.
from numba import prange

PLANT_SEGMENT_DEAD = 0


# @nb.jit(nopython=True, fastmath=True)
def detect_occluded_squares(l: np.array,
                            x_translation: int,
                            y_translation: int,
                            c_id: int,
                            plant_location_array: np.array,
                            occupied_squares):
    x0, y0, x1, y1 = l

    os1x = x0 + x_translation
    os1y = y0 + y_translation
    plant_location_array[os1x, os1y] = c_id

    occupied_squares.add((os1x, os1y, c_id))

    os2x = x1 + x_translation
    os2y = y1 + y_translation
    plant_location_array[os2x, os2y] = c_id

    occupied_squares.add((os2x, os2y, c_id))


# @nb.jit(nopython=True, fastmath=True)
def clear_occluded_square(l: np.array,
                          x_translation: int,
                          y_translation: int,
                          c_id: int,
                          plant_location_array: np.array,
                          occupied_squares):
    x0, y0, x1, y1 = l

    os1x = x0 + x_translation
    os1y = y0 + y_translation
    plant_location_array[os1x, os1y] = 0

    occupied_squares.remove((os1x, os1y, c_id))

    os2x = x1 + x_translation
    os2y = y1 + y_translation
    plant_location_array[os2x, os2y] = 0

    occupied_squares.remove((os2x, os2y, c_id))
