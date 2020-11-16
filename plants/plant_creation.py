import numpy as np

from plants.plant_rendering import detect_occluded_squares

ALIVE_SEGMENT = 1


def generate_random_seedling(num_segs: int, world_params, vicinity: (int, int) = None, parent_creature=None):
    max_x_or_y = world_params['world_size'] - 5
    min_x_or_y: int = 5

    if parent_creature is not None:
        parent_creature['energy'] -= parent_creature['motherhood_cost']

        starting_energy = parent_creature['motherhood_cost']

        # TODO: Add variability and heritability of mutation rate.
        fertile_age = abs(parent_creature['fertile_age'] + np.random.randint(-1, 1))
        child_motherhood_cost = abs(parent_creature['motherhood_cost'] + np.random.randint(-1, 1))

        throw_distance = abs(parent_creature['throw_distance'] + np.random.randint(-1, 1))
        energy_floor_for_growth = abs(parent_creature['energy_floor_for_growth'] + np.random.randint(-1, 1))
        energy_cost_for_growth = abs(parent_creature['energy_cost_for_growth'] + np.random.randint(-1, 1))
        energy_gained_from_one_carbon_dioxide = 200
        energy_cost_per_frame = 1

        lineage = parent_creature['lineage'].copy()
        lineage.append(parent_creature['c_id'])
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
        energy_gained_from_one_carbon_dioxide = 200
        energy_cost_per_frame = 1

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
                            occupied_squares=world_params['occupied_squares'])

    creature = {
        'c_id': plant_id,
        'x_translation': x_translation,
        'y_translation': y_translation,
        'energy': starting_energy,
        'segments': np.array([first_segment]),
        'dead_segments': [],
        'age': 0,
        'fertile_age': fertile_age,
        'alive': True,
        'motherhood_cost': child_motherhood_cost,
        'lineage': lineage,
        'energy_floor_for_growth': energy_floor_for_growth,
        'throw_distance': throw_distance,
        'energy_cost_for_growth': energy_cost_for_growth,
        'energy_gained_from_one_carbon_dioxide': energy_gained_from_one_carbon_dioxide,
        'energy_cost_per_frame': energy_cost_per_frame,
        'num_alive_segments': 1
    }

    world_params['global_creature_id_counter'] = world_params['global_creature_id_counter'] + 1

    return creature, creature['c_id']


def spawn_new_plants(world_params, num_plants: int = 1):
    world_params['all_plants_dictionary'] = {}
    world_params['plants'] = []
    world_params['dead_plants'] = []

    for i in range(num_plants):
        plant, creature_id = generate_random_seedling(1, world_params)
        world_params['all_plants_dictionary'][creature_id] = plant
        world_params['plants'].append(plant)
