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
