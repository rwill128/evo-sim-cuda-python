import numpy as np

from plants.plant_rendering import detect_occluded_squares

ALIVE_SEGMENT = 1


def generate_random_seedling(world_params, vicinity: (int, int) = None, parent_index: int = None):
	max_x_or_y = world_params['world_size'] - 5
	min_x_or_y: int = 5

	if parent_index is not None:
		world_params['alive_plant_energy'][parent_index] -= world_params['motherhood_cost'][parent_index]

		starting_energy = world_params['motherhood_cost'][parent_index]

		# TODO: Add variability and heritability of mutation rate.
		fertile_age = abs(world_params['alive_plant_fertile_ages'][parent_index] + np.random.randint(-1, 1))
		child_motherhood_cost = abs(world_params['motherhood_cost'][parent_index] + np.random.randint(-1, 1))

		throw_distance = abs(world_params['throw_distance'][parent_index] + np.random.randint(-1, 1))
		energy_floor_for_growth = abs(world_params['energy_floor_for_growth'][parent_index] + np.random.randint(-1, 1))
		energy_cost_for_growth = abs(world_params['energy_cost_for_growth'][parent_index] + np.random.randint(-1, 1))
		energy_gained_from_one_carbon_dioxide = abs(world_params['alive_plant_energy_gained_from_one_carbon_dioxide'][parent_index] + np.random.randint(-1, 1))
		energy_cost_per_frame = abs(world_params['energy_cost_per_frame'][parent_index] + np.random.randint(-1, 1))

		# lineage = parent_creature['lineage'].copy()
		# lineage.append(world_params['alive_plant_ids'][parent_index])
	else:
		starting_energy = 1000

		# TODO: Same question as below
		child_motherhood_cost = np.random.randint(10, 10000)
		lineage = []
		fertile_age = np.random.randint(10, 10000)
		throw_distance = np.abs(np.random.randint(10, 10000))
		energy_floor_for_growth = np.random.randint(10, 10000)

		# TODO: What's the tradeoff here? I guess I'm just keeping it random so I can see what a reasonable value is
		energy_cost_for_growth = np.random.randint(10, 10000)
		energy_gained_from_one_carbon_dioxide = np.random.randint(1, 500)
		energy_cost_per_frame = np.random.randint(1, 100)

	if vicinity is None:
		x_translation = np.random.randint(min_x_or_y, max_x_or_y)
	else:
		# TODO: Throw distance should cost energy because it allow parents and children not to interfere with each other. Maybe
		new_location_x_or_min_value = np.max([vicinity[0] + np.random.randint(-throw_distance, np.abs(throw_distance)), min_x_or_y])
		x_translation = np.min([new_location_x_or_min_value, max_x_or_y])

	if vicinity is None:
		y_translation = np.random.randint(5, max_x_or_y)
	else:
		new_location_y_or_min_value = np.max([vicinity[1] + np.random.randint(-throw_distance, throw_distance), min_x_or_y])
		y_translation = np.min([new_location_y_or_min_value, max_x_or_y])

	plant_id = int(world_params['global_creature_id_counter'])
	first_segment = [ALIVE_SEGMENT, 0, 0, np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])]
	detect_occluded_squares(l=first_segment[1:],
							x_translation=x_translation,
							y_translation=y_translation,
							c_id=plant_id,
							plant_location_array=world_params['plant_location_array'],
							world_params=world_params)

	creature = {
			'segments'     : np.array([first_segment]),
			'dead_segments': [],
			# 'lineage'      : lineage,
	}

	# Conversion partially accomplished

	# Conversion fully accomplished
	world_params['alive_plant_ids'] = np.append(world_params['alive_plant_ids'], plant_id)
	world_params['alive_plant_energy'] = np.append(world_params['alive_plant_energy'], starting_energy)
	world_params['alive_plant_fertile_ages'] = np.append(world_params['alive_plant_fertile_ages'], fertile_age)
	world_params['alive_plant_ages'] = np.append(world_params['alive_plant_ages'], int(0))
	world_params['alive_plant_energy_gained_from_one_carbon_dioxide'] = np.append(world_params['alive_plant_energy_gained_from_one_carbon_dioxide'], energy_gained_from_one_carbon_dioxide)
	world_params['energy_cost_for_growth'] = np.append(world_params['energy_cost_for_growth'], energy_cost_for_growth)
	world_params['throw_distance'] = np.append(world_params['throw_distance'], throw_distance)
	world_params['energy_floor_for_growth'] = np.append(world_params['energy_floor_for_growth'], energy_floor_for_growth)
	world_params['energy_cost_per_frame'] = np.append(world_params['energy_cost_per_frame'], energy_cost_per_frame)
	world_params['motherhood_cost'] = np.append(world_params['motherhood_cost'], child_motherhood_cost)
	world_params['num_alive_segments'] = np.append(world_params['num_alive_segments'], int(1))
	world_params['x_translation'] = np.append(world_params['x_translation'], x_translation)
	world_params['y_translation'] = np.append(world_params['y_translation'], y_translation)
	world_params['segments'] = np.append(world_params['segments'], np.array([first_segment]), 0)

	world_params['global_creature_id_counter'] = world_params['global_creature_id_counter'] + 1

	return creature, plant_id


def spawn_new_plants(world_params, num_plants: int = 1):
	world_params['all_plants_dictionary'] = {}
	world_params['plants'] = []
	world_params['dead_plants'] = []

	world_params['alive_plant_ids'] = np.array([], dtype=int)
	world_params['alive_plant_energy'] = np.array([], dtype=int)
	world_params['alive_plant_ages'] = np.array([], dtype=int)
	world_params['alive_plant_fertile_ages'] = np.array([], dtype=int)
	world_params['alive_plant_energy_gained_from_one_carbon_dioxide'] = np.array([], dtype=int)
	world_params['energy_cost_for_growth'] = np.array([], dtype=int)
	world_params['throw_distance'] = np.array([], dtype=int)
	world_params['energy_floor_for_growth'] = np.array([], dtype=int)
	world_params['energy_cost_per_frame'] = np.array([], dtype=int)
	world_params['motherhood_cost'] = np.array([], dtype=int)
	world_params['num_alive_segments'] = np.array([], dtype=int)
	world_params['x_translation'] = np.array([], dtype=int)
	world_params['y_translation'] = np.array([], dtype=int)
	world_params['segments'] = np.empty(shape=(0, 5))

	for i in range(num_plants):
		plant, creature_id = generate_random_seedling(world_params)
		world_params['all_plants_dictionary'][creature_id] = plant
		world_params['plants'].append(plant)
