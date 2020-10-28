import unittest
import numpy as np
import creature_spawning.spawn_creature as sc
import visualization.plant_rendering as pr
import visualization.array_rendering as ar
import simulation.gas_drift as gd
import simulation.plant_simulation as ps
import run_simulation as rs


class RunSimulationTest(unittest.TestCase):
    def test_run_simulation(self):
        world_params = {'world_size': 200,
                        'global_creature_id_counter': int(1)}
        world_params['world_array'] = np.zeros(shape=(world_params['world_size'], world_params['world_size']),
                                               dtype=int)
        world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']),
                                                     fill_value=0)
        sc.spawn_new_plants(world_params=world_params,
                            num_plants=100)

        rs.run_sim_for_x_steps(world_params, 5000)

        ar.render_array(world_params['world_array'], 'Plants')
        ar.render_array(world_params['carbon_dioxide_map'], 'Carbon Dioxide')


if __name__ == '__main__':
    unittest.main()
