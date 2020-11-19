import numpy as np

PLANT_SEGMENT_DEAD = 0


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

    if (os1x, os1y, c_id) in occupied_squares:
        occupied_squares.remove((os1x, os1y, c_id))

    os2x = x1 + x_translation
    os2y = y1 + y_translation

    plant_location_array[os2x, os2y] = 0

    if (os2x, os2y, c_id) in occupied_squares:
        occupied_squares.remove((os2x, os2y, c_id))
