import numpy as np
from numba import njit

PLANT_SEGMENT_DEAD = 0


def detect_occluded_squares(l: np.array,
							x_translation: int,
							y_translation: int,
							c_id: int,
							plant_location_array: np.array,
							world_params):
	x0, y0, x1, y1 = l

	os1x = x0 + x_translation
	os1y = y0 + y_translation
	plant_location_array[os1x, os1y] = c_id

	world_params['occupied_squares_x'] = np.append(world_params['occupied_squares_x'], os1x)
	world_params['occupied_squares_y'] = np.append(world_params['occupied_squares_y'], os1y)
	world_params['occupied_squares_plant_id'] = np.append(world_params['occupied_squares_plant_id'], c_id)

	os2x = x1 + x_translation
	os2y = y1 + y_translation
	plant_location_array[os2x, os2y] = c_id

	if os2x != os1x or os2y != os1y:
		world_params['occupied_squares_x'] = np.append(world_params['occupied_squares_x'], os2x)
		world_params['occupied_squares_y'] = np.append(world_params['occupied_squares_y'], os2y)
		world_params['occupied_squares_plant_id'] = np.append(world_params['occupied_squares_plant_id'], c_id)


def clear_occluded_square(l: np.array,
						  x_translation: int,
						  y_translation: int,
						  c_id: int,
						  plant_location_array: np.array,
						  world_params):
	x0, y0, x1, y1 = l

	os1x = x0 + x_translation
	os1y = y0 + y_translation
	plant_location_array[os1x, os1y] = 0

	indexes_where_x_matches = np.where(world_params['occupied_squares_x'] == os1x)
	indexes_where_y_matches = np.where(world_params['occupied_squares_y'] == os1y)

	indexes_where_plant_id_matches = np.where(world_params['occupied_squares_plant_id'] == c_id)
	indexes_where_x_and_y_matches = np.intersect1d(indexes_where_x_matches, indexes_where_y_matches)
	indexes_where_all_match = np.intersect1d(indexes_where_x_and_y_matches, indexes_where_plant_id_matches)

	accelerated_delete(indexes_where_all_match,
					   world_params['occupied_squares_x'],
					   world_params['occupied_squares_y'],
					   world_params['occupied_squares_plant_id'])


@njit
def accelerated_delete(indexes_where_all_match, occupied_squares_x, occupied_squares_y, occupied_squares_plant_id):
	np.delete(occupied_squares_x, indexes_where_all_match)
	np.delete(occupied_squares_y, indexes_where_all_match)
	np.delete(occupied_squares_plant_id, indexes_where_all_match)
