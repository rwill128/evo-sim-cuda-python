from typing import Callable

import numpy as np
import numba as nb

# TODO: This can be made simpler for plants that are using only ints of length 1. It's just a grid, or it should be
# Probably some or most of this code can be used for animals though.
from numba import prange

PLANT_SEGMENT_DEAD = 0


@nb.jit(nopython=True, fastmath=True)
def detect_occluded_squares(world_array: np.array, l: np.array, cid: float):
    x0, y0, x1, y1 = l

    world_array[int(np.round(x0)), int(np.round(y0))] = cid

    if x1 != x0:
        slope = (y1 - y0) / (x1 - x0)
        length_of_line = np.sqrt((y1 - y0) ** 2 + (x1 - x0) ** 2)
    else:
        slope = 1
        length_of_line = y1 - y0

    if length_of_line == 0:
        step_size = 1
    else:
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
        world_array[int(np.round(x0 + i)), int(np.round(y0 + j))] = cid
        i += x_step_size
        j += y_step_size




@nb.jit(nopython=True, fastmath=True)
def draw_plant(c_id: int, translated_segments: np.array, world_array: np.array):
    l: np.array
    for l in translated_segments:
        if l[0] > PLANT_SEGMENT_DEAD:
            detect_occluded_squares(world_array, l[1:], c_id)


@nb.jit(nopython=True, fastmath=True)
def translate_plant_segs_to_world(segments: np.array, x_translation: int, y_translation: int):
    translated_segments = segments.copy()

    for line in translated_segments:
        if line[0] != PLANT_SEGMENT_DEAD:
            line[1], line[2] = line[1] + x_translation, line[2] + y_translation
            line[3], line[4] = line[3] + x_translation, line[4] + y_translation

    return translated_segments


# This could be heavily optimized for plants because the translations only need to be performed once, and can be stored.
def place_plants(plants, world_array: np.array):
    for plant in plants:
        translated_plant_segments = translate_plant_segs_to_world(
            plant['segments'],
            plant['x_translation'],
            plant['y_translation'])

        draw_plant(plant['c_id'], translated_plant_segments, world_array)


# def place_plants(world_params):
#     for plant in world_params['plants']:
#         translated_plant_segments = translate_plant_segs_to_world(
#             plant['segments'],
#             plant['x_translation'],
#             plant['y_translation'])
#
#         draw_plant(plant['c_id'], translated_plant_segments, world_params['world_array'])

@nb.jit(nopython=True, parallel=True)
def draw_plant_parallel(c_id: int, translated_segments: np.array, world_array: np.array):
    l: np.array
    n = translated_segments.shape[0]
    for i in prange(n):
        l = translated_segments[i]
        if l[0] > PLANT_SEGMENT_DEAD:
            detect_occluded_squares(world_array, l[1:], c_id)

def rotate_vector(x, y, t):
    rot_mat = [[np.cos(t), -np.sin(t)],
               [np.sin(t), np.cos(t)]]
    vector = [[x], [y]]
    rotated_vector = np.matmul(rot_mat, vector)
    return rotated_vector[0, 0], rotated_vector[1, 0]


def translate_creature_segs_to_world(c: np.ndarray) -> np.ndarray:
    translated_c = c.copy()
    x_translation = c[0, 1]
    y_translation = c[0, 2]

    # TODO: Theta and rotation calculations can be skipped for plants as they are currently implemented
    # theta = c[0, 3]

    for line in translated_c[1:]:
        if line[0] > 0:
            # rot_x, rot_y = rotate_vector(line[1], line[2], theta)
            # rot_x2, rot_y2 = rotate_vector(line[3], line[4], theta)
            line[1], line[2] = line[1] + x_translation, line[2] + y_translation
            line[3], line[4] = line[3] + x_translation, line[4] + y_translation

    return translated_c
