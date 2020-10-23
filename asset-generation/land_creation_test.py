import unittest
import land_creation


class LandCreationTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.template = land_creation.create_template(800, 800)
        self.smoothed_template = land_creation.add_smoothing_to_land(self.template)
        self.land, self.water = land_creation.generate_land_and_water_from_template(self.smoothed_template, 0.5)

    def test_create_land(self):
        self.assertEqual(self.template.size, 640000)

    def test_lower_all_land_below_threshold(self):
        self.assertGreaterEqual(self.land.min(), 0.0)
        self.assertLessEqual(self.land.max(), 0.5)
        self.assertGreaterEqual(self.water.min(), -0.5)
        self.assertLessEqual(self.water.max(), 0.0)

    def test_entire_surface(self):
        entire_surface = land_creation.entire_surface(self.land, self.water)


if __name__ == '__main__':
    unittest.main()
