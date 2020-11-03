import numpy as np

ALIVE_SEGMENT = 1

STARTING_PLANT_ENERGY = 1000


def generate_random_seedling(num_segs, world_params):
    creature = {
        'c_id': world_params['global_creature_id_counter'],
        'x_translation': np.random.randint(5, world_params['world_size'] - 5),
        'y_translation': np.random.randint(5, world_params['world_size'] - 5),
        'energy': STARTING_PLANT_ENERGY,
        'segments': np.array([[1, 0, 0, np.random.randint(-1, 1), np.random.randint(-1, 1)]])
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
