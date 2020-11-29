import unittest
import numpy as np
import plants.plant_creation as pc
import run_simulation.simulation as rs


class RunSimulationTest(unittest.TestCase):
	
	def test_run_simulation(self):
		world_params = {'world_size': 1000, 'global_creature_id_counter': int(0)}
		world_params['plant_location_array'] = np.zeros(shape=(world_params['world_size'], world_params['world_size']), dtype=int)
		world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']), fill_value=0)
		
		pc.spawn_new_plants(world_params=world_params, num_plants=5000)
		
		rs.run_sim_for_x_steps(world_dict=world_params, steps=50000)


if __name__ == '__main__':
	unittest.main()
