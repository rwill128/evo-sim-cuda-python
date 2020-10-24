import unittest
import numpy as np
import visualization.creature_rendering as cr


class CreatureRenderingTest(unittest.TestCase):

    def test_rotate_vector(self):
        theta = np.pi / 2
        x = 1
        y = 5
        new_x, new_y = cr.rotate_vector(x, y, theta)

        self.assertEqual(int(new_x), -5)
        self.assertEqual(int(new_y), 1)

        theta = np.pi
        x = 1
        y = 5
        new_x, new_y = cr.rotate_vector(x, y, theta)

        self.assertEqual(int(new_x), -1)
        self.assertEqual(int(new_y), -5)


if __name__ == '__main__':
    unittest.main()
