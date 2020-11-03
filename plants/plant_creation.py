import numpy as np

ALIVE_SEGMENT = 1

STARTING_PLANT_ENERGY = 90


def generate_random_seedling(num_segs: int, world_params, vicinity: (int, int) = None):
    max_x_or_y = world_params['world_size'] - 5
    min_x_or_y: int = 5

    if vicinity is None:
        x_translation = np.random.randint(min_x_or_y, max_x_or_y)
    else:
        new_location_or_min_value = np.max([vicinity[0] + np.random.randint(-10, 10), min_x_or_y])
        x_translation = np.min([new_location_or_min_value, max_x_or_y])

    if vicinity is None:
        y_translation = np.random.randint(5, max_x_or_y)
    else:
        new_location_or_min_value = np.max([vicinity[1] + np.random.randint(-10, 10), min_x_or_y])
        y_translation = np.min([new_location_or_min_value, max_x_or_y])

    creature = {
        'c_id': world_params['global_creature_id_counter'],
        'x_translation': x_translation,
        'y_translation': y_translation,
        'energy': STARTING_PLANT_ENERGY,
        'segments': np.array([[1, 0, 0, np.random.randint(-1, 1), np.random.randint(-1, 1)]]),
        'age': 0,
        'fertile_age': 1000,
        'alive': True
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

    return creature


def spawn_new_plants(world_params, num_plants: int = 1):
    new_plants = []

    for i in range(num_plants):
        plant = generate_random_seedling(1, world_params)
        new_plants.append(plant)

    world_params['plants'] = new_plants
    world_params['dead_plants'] = []
