import unittest
import numpy as np
import plants.plant_creation as pc
import plants.plant_rendering as pr
import run_simulation.simulation as rs
import asset_generation.land_creation as lc

# World map array indices
PLANT_LOCATION_ARRAY_INDEX = 0
CARBON_DIOXIDE_ARRAY_INDEX = 1

# World info array indices
WORLD_SIZE_INDEX = 0
PLANT_ID_COUNTER_INDEX = 1


class RunSimulationTest(unittest.TestCase):

    def test_run_simulation(self):
        world_dictionary = self.create_world_dictionary()
        world_info_array, world_map_array = self.create_world_array()

        pc.spawn_new_plants(world_dictionary=world_dictionary,
                            num_plants=500)
        pr.place_plants(world_dictionary)

        rs.run_sim_for_x_steps(world_dictionary, 10000)

    def create_world_dictionary(self):
        world_dictionary = {'world_size': 200,
                            'global_creature_id_counter': int(1)}
        world_dictionary['plant_location_array'] = np.zeros(
            shape=(world_dictionary['world_size'], world_dictionary['world_size']),
            dtype=int)
        world_dictionary['carbon_dioxide_map'] = np.full(
            shape=(world_dictionary['world_size'], world_dictionary['world_size']),
            fill_value=0)
        return world_dictionary

    def create_world_array(self):
        world_info_array = np.array([200, 1])
        world_map_array = [
            np.zeros(shape=(world_info_array[WORLD_SIZE_INDEX], world_info_array[WORLD_SIZE_INDEX]), dtype=int),
            np.zeros(shape=(world_info_array[WORLD_SIZE_INDEX], world_info_array[WORLD_SIZE_INDEX]), dtype=int)
        ]

        return world_info_array, world_map_array


if __name__ == '__main__':
    unittest.main()
