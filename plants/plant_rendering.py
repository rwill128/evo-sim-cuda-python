from typing import Callable

import numpy as np
import numba as nb

# TODO: This can be made simpler for plants that are using only ints of length 1. It's just a grid, or it should be
# Probably some or most of this code can be used for animals though.
from numba import prange

PLANT_SEGMENT_DEAD = 0


@nb.jit(nopython=True)
def detect_occluded_squares(world_array: np.array, l: np.array, x_translation: int, y_translation: int, cid: int):
    x0, y0, x1, y1 = l
    world_array[x0 + x_translation, y0 + y_translation] = cid
    world_array[x1 + x_translation, y1 + y_translation] = cid

@nb.jit(nopython=True)
def draw_plant(c_id: int, segments: np.array, x_translation: int, y_translation: int, world_array: np.array):
    for l in segments:
        if l[0] > PLANT_SEGMENT_DEAD:
            detect_occluded_squares(world_array, l[1:], x_translation, y_translation, c_id)


# This could be heavily optimized for plants because the translations only need to be performed once, and can be stored.
def place_plants(world_params):
    for plant in world_params['plants']:
        draw_plant(plant['c_id'], plant['segments'], plant['x_translation'], plant['y_translation'],
                   world_params['world_array'])
