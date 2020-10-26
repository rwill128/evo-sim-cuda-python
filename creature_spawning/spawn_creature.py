import numpy as np


def generate_random_simple_creature(num_segs, world_params):
    c_id = world_params['global_creature_id_counter']

    world_params['global_creature_id_counter'] = world_params['global_creature_id_counter'] + 1

    # Top row for info, other rows for segments
    sc = np.zeros(shape=(num_segs + 1, 5))

    # Generates an array that looks like this:
    #   c_id x_t  y_t  energy
    # [[ 0.,  0.,  0.,  0.,  0.],
    #    [ 0.,  0.,  0., -1.,  0.]]

    # Assign Id
    sc[0, 0] = c_id
    sc[1] = [1, 0, 0, np.random.randint(-1, 1), np.random.randint(-1, 1)]
    if num_segs > 1:
        for i in range(2, num_segs + 1):
            sc[i] = [1, sc[i - 1, 3], sc[i - 1, 4], sc[i - 1, 3] + np.random.randint(-1, 1),
                     sc[i - 1, 4] + np.random.randint(-1, 1)]

    return sc


def spawn_new_plants(world_params, num_plants: int = 1):
    new_plants = []

    for i in range(num_plants):
        plant = generate_random_simple_creature(1, world_params)
        plant[0, 1] = np.random.randint(2, world_params['world_size'] - 2)
        plant[0, 2] = np.random.randint(2, world_params['world_size'] - 2)
        new_plants.append(plant)

    return new_plants
