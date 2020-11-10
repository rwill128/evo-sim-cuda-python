import unittest
import numpy as np
import plants.plant_creation as pc
import plants.plant_rendering as pr
import run_simulation.simulation as rs
import asset_generation.land_creation as lc
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os

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

        world_params['plant_location_array'] = np.zeros(shape=(world_params['world_size'], world_params['world_size']),
                                               dtype=int)
        world_params['carbon_dioxide_map'] = np.full(shape=(world_params['world_size'], world_params['world_size']),
                                                     fill_value=0)
        pc.spawn_new_plants(world_params=world_params,
                            num_plants=500)
        pr.place_plants(world_params)

        rs.run_sim_for_x_steps(world_params, 10000)

        fig, axs = plt.subplots(2, 2)

        axs[0, 0].title.set_text('Plant Locations')
        axs[0, 0].imshow(world_params['plant_location_array'], interpolation='nearest', cmap=cm.Greens)

        axs[1, 0].title.set_text("Carbon Dioxide")
        axs[1, 0].imshow(world_params['carbon_dioxide_map'], interpolation='nearest', cmap=cm.Greys)

        axs[0, 1].title.set_text("Land")
        axs[0, 1].imshow(world_params['land_array'], interpolation='nearest', cmap=cm.Oranges)

        axs[1, 1].title.set_text("Water")
        axs[1, 1].imshow(world_params['water_array'], interpolation='nearest', cmap=cm.Blues)

        fig.set_size_inches(10, 10)
        fig.tight_layout()

        fig.savefig(os.path.join(os.path.curdir, 'build-artifacts/world-results.png'), dpi=100)
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
