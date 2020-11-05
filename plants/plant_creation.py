import numpy as np

ALIVE_SEGMENT = 1

def generate_random_seedling(num_segs: int, world_params, vicinity: (int, int) = None, parent_creature = None):
    max_x_or_y = world_params['world_size'] - 5
    min_x_or_y: int = 5

    if parent_creature is not None:
        starting_energy = parent_creature['motherhood_cost']
        parent_creature['energy'] -= parent_creature['motherhood_cost']

        fertile_age = parent_creature['fertile_age'] + np.random.randint(-1, 1)
        child_motherhood_cost = parent_creature['motherhood_cost'] + np.random.randint(-1, 1)
        throw_distance = parent_creature['throw_distance'] + np.random.randint(-1, 1)

        lineage = parent_creature['lineage'].copy()
        lineage.append(parent_creature['c_id'])
    else:
        starting_energy = 1000
        child_motherhood_cost = np.random.randint(10, 10000)
        lineage = []
        fertile_age = np.random.randint(10, 10000)
        throw_distance = np.random.randint(10, 10000)


    if vicinity is None:
        x_translation = np.random.randint(min_x_or_y, max_x_or_y)
    else:
        # TODO: Throw distance should cost energy because it allow parents and children not to interfere with each other
        new_location_or_min_value = np.max([vicinity[0] + np.random.randint(-10, 10), min_x_or_y])
        x_translation = np.min([new_location_or_min_value, max_x_or_y])

    if vicinity is None:
        y_translation = np.random.randint(5, max_x_or_y)
    else:
        new_location_or_min_value = np.max([vicinity[1] + np.random.randint(-10, 10), min_x_or_y])
        y_translation = np.min([new_location_or_min_value, max_x_or_y])

    creature = {
        'c_id': int(world_params['global_creature_id_counter']),
        'x_translation': x_translation,
        'y_translation': y_translation,
        'energy': starting_energy,
        'segments': np.array([[1, 0, 0, np.random.randint(-1, 1), np.random.randint(-1, 1)]]),
        'age': 0,
        'fertile_age': fertile_age,
        'alive': True,
        'motherhood_cost': child_motherhood_cost,
        'lineage': lineage,
        'energy_floor_for_growth': np.random.randint(10, 10000),
        'throw_distance': throw_distance
    }

    world_params['global_creature_id_counter'] = world_params['global_creature_id_counter'] + 1

    # Assign Id
    if num_segs > 1:
        for i in range(1, num_segs):
            creature['segments'][i] = [
                ALIVE_SEGMENT,
                creature['segments'][i - 1, 3],  # Starts off previous segment's endpoint
                creature['segments'][i - 1, 4],
                creature['segments'][i - 1, 3] + np.random.randint(-1, 1),  # Ends in a random place close by.
                creature['segments'][i - 1, 4] + np.random.randint(-1, 1)]
            # TODO: ^^ This is where gene-based growth patterns would be implemented

    return creature, creature['c_id']


def spawn_new_plants(world_params, num_plants: int = 1):
    world_params['all_plants_dictionary'] = {}
    world_params['plants'] = []
    world_params['dead_plants'] = []

    for i in range(num_plants):
        plant, creature_id = generate_random_seedling(1, world_params)
        world_params['all_plants_dictionary'][creature_id] = plant
        world_params['plants'].append(plant)
