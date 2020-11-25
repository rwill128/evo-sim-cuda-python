import numpy as np
from numba import njit, jit

PLANT_SEGMENT_DEAD = 0


@njit(cache=True)
def detect_occluded_squares(x0: int, y0: int, x1: int, y1: int,
                            x_translation: int,
                            y_translation: int,
                            c_id: int,
                            plant_location_array: np.ndarray):
	plant_location_array[int(x0 + x_translation), int(y0 + y_translation)] = c_id
	if x1 != x0 or y1 != y0:
		plant_location_array[int(x1 + x_translation), int(y1 + y_translation)] = c_id


@njit(cache=True)
def clear_occluded_square(x0, y0, x1, y1,
                          x_translation: int,
                          y_translation: int,
                          plant_location_array: np.array):
	os1x = x0 + x_translation
	os1y = y0 + y_translation
	plant_location_array[os1x, os1y] = 0
	
	if x1 != x0 or y1 != y0:
		os2x = x0 + x_translation
		os2y = y0 + y_translation
		plant_location_array[os2x, os2y] = 0
