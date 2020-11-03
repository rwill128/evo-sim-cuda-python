def translate_creature_segs_to_world(c: np.ndarray) -> np.ndarray:
    translated_c = c.copy()
    x_translation = c[0, 1]
    y_translation = c[0, 2]

    # TODO: Theta and rotation calculations can be skipped for plants as they are currently implemented
    # theta = c[0, 3]

    for line in translated_c[1:]:
        if line[0] > 0:
            # rot_x, rot_y = rotate_vector(line[1], line[2], theta)
            # rot_x2, rot_y2 = rotate_vector(line[3], line[4], theta)
            line[1], line[2] = line[1] + x_translation, line[2] + y_translation
            line[3], line[4] = line[3] + x_translation, line[4] + y_translation

    return translated_c


def rotate_vector(x, y, t):
    rot_mat = [[np.cos(t), -np.sin(t)],
               [np.sin(t), np.cos(t)]]
    vector = [[x], [y]]
    rotated_vector = np.matmul(rot_mat, vector)
    return rotated_vector[0, 0], rotated_vector[1, 0]
