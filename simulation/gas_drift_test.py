import unittest
import numpy as np

import simulation.gas_drift as gd
import visualization.array_rendering as ar

class GasDriftTest(unittest.TestCase):
    def test_gas_drift(self):
        world_params = {
            'world_size': 1000
        }
        world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']),
                                                     fill_value=0)
        for i in range(3000):

            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .25)][int(world_params['world_size'] * .25)] += 1
            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .25)][int(world_params['world_size'] * .75)] += 1
            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .75)][int(world_params['world_size'] * .25)] += 1
            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .75)][int(world_params['world_size'] * .75)] += 1

            gd.move_gases(world_params['carbon_dioxide_map'], world_params['world_size'])

        # ar.render_array(world_params['carbon_dioxide_map'], 'Carbon Dioxide')



if __name__ == '__main__':
    unittest.main()
