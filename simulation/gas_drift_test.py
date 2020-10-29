import unittest
import numpy as np
from scipy.sparse import csc_matrix

import simulation.gas_drift as gd
import visualization.array_rendering as ar
import scipy.sparse as sparse


class GasDriftTest(unittest.TestCase):
    def test_gas_drift(self):
        world_params = {
            'world_size': 100
        }
        world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']),
                                                     fill_value=0)
        for i in range(1000):
            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .25)][
                int(world_params['world_size'] * .25)] += 1
            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .25)][
                int(world_params['world_size'] * .75)] += 1
            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .75)][
                int(world_params['world_size'] * .25)] += 1
            world_params['carbon_dioxide_map'][int(world_params['world_size'] * .75)][
                int(world_params['world_size'] * .75)] += 1

            gd.move_gases(world_params['carbon_dioxide_map'], world_params['world_size'])

        ar.render_array(world_params['carbon_dioxide_map'], 'Carbon Dioxide')

    def test_gas_drift_scipy_sparse_matrix(self):
        world_params = {
            'world_size': 100
        }

        carbon_additions_each_frame = np.full(shape=(world_params['world_size'], world_params['world_size']),
                                              fill_value=0)
        carbon_additions_each_frame[int(world_params['world_size'] * .25)][int(world_params['world_size'] * .25)] += 1
        carbon_additions_each_frame[int(world_params['world_size'] * .25)][int(world_params['world_size'] * .75)] += 1
        carbon_additions_each_frame[int(world_params['world_size'] * .75)][int(world_params['world_size'] * .25)] += 1
        carbon_additions_each_frame[int(world_params['world_size'] * .75)][int(world_params['world_size'] * .75)] += 1

        world_params['carbon_dioxide_map'] = sparse.csc_matrix((world_params['world_size'], world_params['world_size']),
                                                               dtype=int)
        carbon_additions_each_frame_sparse_matrix: csc_matrix = sparse.csc_matrix(carbon_additions_each_frame)

        for i in range(50):
            world_params['carbon_dioxide_map'] = world_params['carbon_dioxide_map'] + carbon_additions_each_frame_sparse_matrix

            world_params['carbon_dioxide_map'] = gd.move_gases_scipy_sparse_matrix(world_params['carbon_dioxide_map'], world_params['world_size'])

        ar.render_array(world_params['carbon_dioxide_map'].toarray(), 'Carbon Dioxide')


if __name__ == '__main__':
    unittest.main()
