import numpy as np


def generate_random_simple_creature(num_segs, global_creature_id_counter):
    c_id = ++global_creature_id_counter

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


def spawn_new_plants(world_size, num_plants: int = 1, global_creature_id_counter: int = 0):
    new_plants = []

    for i in range(num_plants):
        plant = generate_random_simple_creature(1, global_creature_id_counter)
        plant[0, 1] = np.random.randint(2, world_size - 2)
        plant[0, 2] = np.random.randint(2, world_size - 2)
        new_plants.append(plant)

    return new_plants
