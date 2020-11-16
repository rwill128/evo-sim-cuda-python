from typing import Callable

import numpy as np
import numba as nb

# TODO: This can be made simpler for plants that are using only ints of length 1. It's just a grid, or it should be
# Probably some or most of this code can be used for animals though.
from numba import prange

PLANT_SEGMENT_DEAD = 0


# @nb.jit(nopython=True, fastmath=True)
def detect_occluded_squares(l: np.array, x_translation: int, y_translation: int, c_id: int,
                            plant_location_array: np.array):
    x0, y0, x1, y1 = l
    plant_location_array[x0 + x_translation, y0 + y_translation] = c_id
    plant_location_array[x1 + x_translation, y1 + y_translation] = c_id


# @nb.jit(nopython=True, fastmath=True)
def clear_occluded_square(l: np.array, x_translation: int, y_translation: int, plant_location_array: np.array):
    x0, y0, x1, y1 = l
    plant_location_array[x0 + x_translation, y0 + y_translation] = 0
    plant_location_array[x1 + x_translation, y1 + y_translation] = 0