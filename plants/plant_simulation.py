import numpy as np
from numba import njit, jit

from plants.plant_creation import generate_random_seedling
from plants.plant_rendering import PLANT_SEGMENT_DEAD, detect_occluded_squares, clear_occluded_square

# @jit(cache=True)
def grow_plants(world_params):
	vectorized_grow_plants(world_params)
	vectorized_kill_plants(world_params)

	no_energy_indexes = np.where(world_params['alive_plant_energy'] <= 0)[0]
	if len(no_energy_indexes) > 0:
		vectorized_kill_segments = np.vectorize(kill_segments)
		vectorized_kill_segments(no_energy_indexes, world_params)

	indexes_where_plants_have_reached_fertile_age = np.where(np.greater(world_params['alive_plant_ages'], world_params['alive_plant_fertile_ages']) == True)
	indexes_where_plants_have_enough_energy_for_motherhood_cost = np.where(np.greater(world_params['alive_plant_energy'], world_params['motherhood_cost']) == True)
	reproduction_indexes = np.intersect1d(indexes_where_plants_have_reached_fertile_age, indexes_where_plants_have_enough_energy_for_motherhood_cost)

	if len(reproduction_indexes) > 0:
		vectorized_add_babies = np.vectorize(add_babies)
		vectorized_add_babies(reproduction_indexes, world_params)

	new_growth = []
	for index, plant_id in enumerate(world_params['alive_plant_ids']):
		plant = world_params['plants'][index]
		add_new_growth(index, new_growth, plant, world_params)

	for index, new_segment in new_growth:
		world_params['num_alive_segments'][index] += 1
		world_params['plants'][index]['segments'] = np.append(world_params['plants'][index]['segments'], [new_segment], 0)


# @jit(cache=True)
def add_babies(index, world_params):
	seedling, seedling_id = generate_random_seedling(world_params, (world_params['x_translation'][index], world_params['y_translation'][index]), index)
	world_params['all_plants_dictionary'][seedling_id] = seedling
	world_params['plants'].append(seedling)


# @jit(cache=True)
def add_new_growth(index, new_growth, plant, world_params):
	if world_params['alive_plant_energy'][index] > world_params['energy_floor_for_growth'][index] \
			and world_params['alive_plant_ages'][index] < world_params['alive_plant_fertile_ages'][index]\
			and world_params['num_alive_segments'][index] > 1:
		world_params['alive_plant_energy'][index] -= world_params['energy_cost_for_growth'][index]
		joined_seg = plant['segments'][np.random.randint(0, world_params['num_alive_segments'][index])]  # TODO: Should only grow off of live segments
		new_seg = [
				1,
				joined_seg[3],
				joined_seg[4],
				joined_seg[3] + np.random.choice([-1, 0, 1]),
				joined_seg[4] + np.random.choice([-1, 0, 1])]
		detect_occluded_squares(joined_seg[1], joined_seg[2], joined_seg[3], joined_seg[4],
								x_translation=world_params['x_translation'][index],
								y_translation=world_params['y_translation'][index],
								c_id=world_params['alive_plant_ids'][index],
								plant_location_array=world_params['plant_location_array'],)
		new_growth.append((index, new_seg))

# @jit(cache=True)
def kill_segments(index, world_params):
	plant = world_params['plants'][index]
	if world_params['alive_plant_energy'][index] <= 0:
		if world_params['num_alive_segments'][index] == 1:
			# Mark only segment dead
			only_segment = plant['segments'][0]
			clear_occluded_square(only_segment[1], only_segment[2], only_segment[3], only_segment[4],
								  x_translation=world_params['x_translation'][index],
								  y_translation=world_params['y_translation'][index],
								  plant_location_array=world_params['plant_location_array'])
			only_segment[0] = PLANT_SEGMENT_DEAD
			plant['segments'] = np.delete(plant['segments'], 0, 0)
			plant['dead_segments'].append(only_segment)
			world_params['num_alive_segments'][index] = 0
		if world_params['num_alive_segments'][index] > 1:
			# Mark random segment dead
			segment_to_kill_index = np.random.randint(0, world_params['num_alive_segments'][index])
			segment_to_kill = plant['segments'][segment_to_kill_index]
			clear_occluded_square(l=segment_to_kill[1:],
								  x_translation=world_params['x_translation'][index],
								  y_translation=world_params['y_translation'][index],
								  c_id=world_params['alive_plant_ids'][index],
								  plant_location_array=world_params['plant_location_array'],
								  world_params=world_params)
			segment_to_kill[0] = PLANT_SEGMENT_DEAD
			plant['segments'] = np.delete(plant['segments'], segment_to_kill_index, 0)
			plant['dead_segments'].append(segment_to_kill)
			world_params['num_alive_segments'][index] -= 1

# @njit(cache=True)
def vectorized_grow_plants(world_params):
	world_params['alive_plant_ages'] += 1
	world_params['alive_plant_energy'] = world_params['alive_plant_energy'] - (world_params['num_alive_segments'] * world_params['energy_cost_per_frame'])

# @jit(cache=True)
def vectorized_kill_plants(world_params):
	no_energy = np.where(world_params['alive_plant_energy'] <= 0)
	no_segments = np.where(world_params['num_alive_segments'] <= 0)
	dead_indexes = np.intersect1d(no_energy, no_segments)
	if len(dead_indexes) > 0:
		world_params['alive_plant_ids'] = np.delete(world_params['alive_plant_ids'], dead_indexes, 0)
		world_params['alive_plant_energy'] = np.delete(world_params['alive_plant_energy'], dead_indexes, 0)
		world_params['alive_plant_ages'] = np.delete(world_params['alive_plant_ages'], dead_indexes, 0)
		world_params['alive_plant_fertile_ages'] = np.delete(world_params['alive_plant_fertile_ages'], dead_indexes, 0)
		world_params['alive_plant_energy_gained_from_one_carbon_dioxide'] = np.delete(world_params['alive_plant_energy_gained_from_one_carbon_dioxide'], dead_indexes, 0)
		world_params['energy_cost_for_growth'] = np.delete(world_params['energy_cost_for_growth'], dead_indexes, 0)
		world_params['throw_distance'] = np.delete(world_params['throw_distance'], dead_indexes, 0)
		world_params['energy_floor_for_growth'] = np.delete(world_params['energy_floor_for_growth'], dead_indexes, 0)
		world_params['energy_cost_per_frame'] = np.delete(world_params['energy_cost_per_frame'], dead_indexes, 0)
		world_params['motherhood_cost'] = np.delete(world_params['motherhood_cost'], dead_indexes, 0)
		world_params['x_translation'] = np.delete(world_params['x_translation'], dead_indexes, 0)
		world_params['y_translation'] = np.delete(world_params['y_translation'], dead_indexes, 0)
		world_params['num_alive_segments'] = np.delete(world_params['num_alive_segments'], dead_indexes, 0)
	for index in dead_indexes[::-1]:
		del world_params['plants'][index]

# @jit(cache=True)
def photosynthesize(plant_location_array, carbon_dioxide_map, alive_plant_ids, alive_plant_energy, alive_plant_energy_gained_from_one_carbon_dioxide):
	boolean_mask_of_both_presence = accelerated_photosynthesis_one(carbon_dioxide_map, plant_location_array)

	carbon_dioxide_map[boolean_mask_of_both_presence] -= 1

	global_indices_of_plants_gaining_energy_this_frame = accelerated_where(np.in1d(alive_plant_ids, plant_location_array[boolean_mask_of_both_presence]))

	alive_plant_energy[global_indices_of_plants_gaining_energy_this_frame] = \
		alive_plant_energy[global_indices_of_plants_gaining_energy_this_frame] \
		+ alive_plant_energy_gained_from_one_carbon_dioxide[global_indices_of_plants_gaining_energy_this_frame]

# @jit(cache=True)
def accelerated_where(in1d_var):
	frame = np.where(in1d_var)[0]
	return frame

@jit(cache=True)
def accelerated_photosynthesis_one(carbon_dioxide_map, plant_location_array):
	return np.logical_and(plant_location_array, carbon_dioxide_map)
