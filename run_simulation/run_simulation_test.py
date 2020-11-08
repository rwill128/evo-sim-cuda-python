import unittest
import numpy as np
import plants.plant_creation as pc
import plants.plant_rendering as pr
import run_simulation.simulation as rs


class RunSimulationTest(unittest.TestCase):

    # TODO: Should really convert everything to numpy arrays, which I can access with constants in a dictionary-like way. This will improve performance a lot, allow numba use, and allow conversion to CUDA much more easily
    def test_run_simulation(self):
        world_params = {'world_size': 200,
                        'global_creature_id_counter': int(1)}
        world_params['world_array'] = np.zeros(shape=(world_params['world_size'], world_params['world_size']),
                                               dtype=int)
        world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']),
                                                     fill_value=0)
        pc.spawn_new_plants(world_params=world_params,
                            num_plants=500)
        pr.place_plants(world_params)

        rs.run_sim_for_x_steps(world_params, 10000)


if __name__ == '__main__':
    unittest.main()
