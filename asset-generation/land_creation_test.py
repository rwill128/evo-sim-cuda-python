import sys
import unittest
import land_creation


class LandCreationTestCase(unittest.TestCase):
    def test_create_land(self):
        print(sys.path)
        land = land_creation.create_land()
        self.assertEqual(land.size, 640000)


if __name__ == '__main__':
    unittest.main()
