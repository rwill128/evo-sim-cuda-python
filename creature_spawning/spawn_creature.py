import numpy as np


def generate_random_simple_creature():

    c_id = 1
    num_segs = 1

    # Top row for info, other rows for segments
    sc = np.zeros(shape=(num_segs + 1, 5))

    # Generates an array that looks like this:
    #   c_id x_t  y_t  theta
    # [[ 0.,  0.,  0.,  0.,  0.],
    #    [ 0.,  0.,  0., -1.,  0.]]

    # Assign Id
    sc[0,0] = c_id
    sc[1] = [0.1, 0.0, 0.0, float(np.random.randint(-1, 1)), float(np.random.randint(-1, 1))]
    # sc[2] = [0.1, sc[1,3], sc[1,4], sc[1,3] + float(np.random.randint(-1, 1)), sc[1,4] + float(np.random.randint(-1, 1))]
    # sc[3] = [0.1, sc[2,3], sc[2,4], sc[2,3] + float(np.random.randint(-1, 1)), sc[2,4] + float(np.random.randint(-1, 1))]
    # sc[3] = [0.1, sc[3,3], sc[3,4], sc[3,3] + float(np.random.randint(-1, 1)), sc[3,4] + float(np.random.randint(-1, 1))]

    return sc