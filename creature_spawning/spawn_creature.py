import numpy as np


def generate_random_simple_creature(num_segs=1):
    c_id = 1

    # Top row for info, other rows for segments
    sc = np.zeros(shape=(num_segs + 1, 5))

    # Generates an array that looks like this:
    #   c_id x_t  y_t  theta
    # [[ 0.,  0.,  0.,  0.,  0.],
    #    [ 0.,  0.,  0., -1.,  0.]]

    # Assign Id
    sc[0, 0] = c_id
    sc[1] = [0.1, 0.0, 0.0, float(np.random.randint(-1, 1)), float(np.random.randint(-1, 1))]
    if num_segs > 1:
        for i in range(2, num_segs + 1):
            sc[i] = [0.1, sc[i - 1, 3], sc[i - 1, 4], sc[i - 1, 3] + float(np.random.randint(-1, 1)),
                     sc[i - 1, 4] + float(np.random.randint(-1, 1))]

    return sc


def spawn_new_plants(num_plants: int = 1):

    new_plants = []

    for i in range(num_plants):
        plant = sc.generate_random_simple_creature(1)
        plant[0,1] = np.random.randint(2,world_size-2)
        plant[0,2] = np.random.randint(2,world_size-2)
        plant[0,3] = np.random.random_sample() * np.pi * 2
        new_plants.append(plant)

    return new_plants