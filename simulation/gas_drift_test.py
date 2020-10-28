import unittest
import numpy as np

from simulation.gas_drift import move_gases


class GasDriftTest(unittest.TestCase):
    def test_gas_drift(self):
        world_params = {
            'world_size': 1000
        }
        world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']),
                                                     fill_value=0)
        for i in range(1000):

            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .25)][int(world_params['world_size'] * .25)] += 1
            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .25)][int(world_params['world_size'] * .75)] += 1
            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .75)][int(world_params['world_size'] * .25)] += 1
            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .75)][int(world_params['world_size'] * .75)] += 1

            move_gases(world_params)

if __name__ == '__main__':
    unittest.main()
