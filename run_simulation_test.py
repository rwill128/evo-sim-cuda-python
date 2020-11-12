import unittest
import numpy as np
import plants.plant_creation as pc
import plants.plant_rendering as pr
import run_simulation.simulation as rs
import asset_generation.land_creation as lc


class RunSimulationTest(unittest.TestCase):

    # TODO: Should really convert everything to numpy arrays, which I can access with constants in a dictionary-like way. This will improve performance a lot, allow numba use, and allow conversion to CUDA much more easily
    def test_run_simulation(self):
        world_params = {'world_size': 200,
                        'global_creature_id_counter': int(1)}

        template = lc.create_template(200, 200)
        smoothed_template = lc.add_smoothing_to_template(template)
        land, water = lc.generate_land_and_water_from_template(smoothed_template, 0.4)
        entire_surface = lc.entire_surface(land, water)

        world_params['land_array'] = land
        world_params['water_array'] = water
        world_params['plant_surface_area_history'] = {'time': [], 'plant_surface_area_history': []}
        world_params['carbon_dioxide_amount_history'] = {'time': [], 'carbon_dioxide_amount_history': []}
        world_params['population'] = {'time': [], 'population': []}

        world_params['plant_location_array'] = np.zeros(shape=(world_params['world_size'], world_params['world_size']),
                                                        dtype=int)
        world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']),
                                                     fill_value=0)
        pc.spawn_new_plants(world_params=world_params,
                            num_plants=500)
        pr.place_plants(world_params)

        rs.run_sim_for_x_steps(world_params, 200000)


if __name__ == '__main__':
    unittest.main()
