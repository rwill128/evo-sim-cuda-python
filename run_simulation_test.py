import unittest
import numpy as np
import plants.plant_creation as pc
import run_simulation.simulation as rs
import asset_generation.land_creation as lc


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
        world_params['occupied_squares'] = set()

        world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']), fill_value=0)

        pc.spawn_new_plants(world_params=world_params, num_plants=5000)

        rs.run_sim_for_x_steps(world_dict=world_params, steps=5000)

        pass


if __name__ == '__main__':
    unittest.main()
