import unittest
import numpy as np
from numba import njit

import plants.plant_creation as pc
import run_simulation.simulation as rs
import asset_generation.land_creation as lc
import line_profiler

profiler = line_profiler.LineProfiler()


class RunSimulationTest(unittest.TestCase):
	
	def test_run_simulation(self):
		world_params = {'world_size': 200, 'global_creature_id_counter': int(0)}
		
		template = lc.create_template(world_params['world_size'], world_params['world_size'])
		smoothed_template = lc.add_smoothing_to_template(template)
		land, water = lc.generate_land_and_water_from_template(smoothed_template, 0.4)
		
		world_params['land_array'] = land
		world_params['water_array'] = water
		world_params['plant_surface_area_history'] = {'time': [], 'plant_surface_area_history': []}
		world_params['carbon_dioxide_amount_history'] = {'time': [], 'carbon_dioxide_amount_history': []}
		world_params['population'] = {'time': [], 'population': []}
		
		world_params['plant_location_array'] = np.zeros(shape=(world_params['world_size'], world_params['world_size']), dtype=int)
		world_params['occupied_squares_x'] = np.array([], dtype=int)
		world_params['occupied_squares_y'] = np.array([], dtype=int)
		world_params['occupied_squares_plant_id'] = np.array([], dtype=int)
		
		world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']), fill_value=0)
		
		pc.spawn_new_plants(world_params=world_params, num_plants=5000)
		
		rs.run_sim_for_x_steps(world_dict=world_params, steps=5000)
		
		pass
	
	def test_old_2d_photosynthesis(self):
		plant_location_array = np.random.randint(0, 2, size=(200, 200), dtype=int)
		carbon_location_array = np.random.randint(0, 2, size=(200, 200), dtype=int)
		old_2d_photosynthesis(plant_location_array=plant_location_array,
		                      carbon_location_array=carbon_location_array)
	
	def test_nonzero_photosynthesis(self):
		plant_location_array = np.random.randint(0, 2, size=(200, 200), dtype=int)
		carbon_location_array = np.random.randint(0, 2, size=(200, 200), dtype=int)
		boolean_mask_of_both = nonzero_photosynthesis(plant_location_array=plant_location_array,
		                                              carbon_location_array=carbon_location_array)
		profiler.print_stats()


def old_2d_photosynthesis(plant_location_array, carbon_location_array):
	boolean_mask_of_plant_presence = plant_location_array > 0
	boolean_mask_of_carbon_presence = carbon_location_array > 0
	return np.logical_and(boolean_mask_of_carbon_presence, boolean_mask_of_plant_presence)


def nonzero_photosynthesis(plant_location_array: np.ndarray, carbon_location_array: np.ndarray):
	return np.logical_and(plant_location_array, carbon_location_array)


def new_1d_photosynthesis(plant_location_array, carbon_location_array):
	boolean_mask_of_plant_presence = plant_location_array > 0
	boolean_mask_of_carbon_presence = carbon_location_array > 0
	return np.logical_and(boolean_mask_of_carbon_presence, boolean_mask_of_plant_presence)


if __name__ == '__main__':
	unittest.main()
