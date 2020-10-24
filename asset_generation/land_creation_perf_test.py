import unittest
import timeit


class LandCreationPerfTestCase(unittest.TestCase):
    def test_create_template(self):
        t = timeit.timeit('import land_creation; land_creation.create_template(800, 800)', number=10)
        self.assertLessEqual(t / 10, 0.07)


if __name__ == '__main__':
    unittest.main()
