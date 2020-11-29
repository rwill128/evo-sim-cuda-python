import unittest
import numpy as np
import plants.plant_creation as pc
import run_simulation.simulation as rs
import pickle

class RunSimulationTest(unittest.TestCase):
	
	def test_run_simulation(self):

		load_game = open('C:\evo-sim-records\saves\game_state.obj', 'rb')
		world_params = pickle.load(load_game)

		if world_params['world_size'] != 1000:
			world_params = {'world_size': 1000, 'global_creature_id_counter': int(0)}
			world_params['plant_location_array'] = np.zeros(shape=(world_params['world_size'], world_params['world_size']), dtype=int)
			world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']), fill_value=0)
		
		pc.spawn_new_plants(world_params=world_params, num_plants=5000)
		rs.run_sim_for_x_steps(world_dict=world_params, steps=2000)

		# Save game:
		save_game = open('C:\evo-sim-records\saves\game_state.obj', 'wb')
		pickle.dump(world_params, save_game)


if __name__ == '__main__':
	unittest.main()
