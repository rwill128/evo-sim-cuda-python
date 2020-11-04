import numpy as np
import plants.plant_rendering as pr
import simulation.gas_drift as gd
import plants.plant_simulation as ps


def run_sim_for_x_steps(world, steps):
    for i in range(steps):
        world['world_array'] = np.zeros(shape=(world['world_size'], world['world_size']), dtype=int)
        # TODO: Make it so that these points drift every 100 frames or so.
        world['carbon_dioxide_map'][int(world['world_size'] * .25)][int(world['world_size'] * .25)] += 1
        world['carbon_dioxide_map'][int(world['world_size'] * .25)][int(world['world_size'] * .75)] += 1
        world['carbon_dioxide_map'][int(world['world_size'] * .75)][int(world['world_size'] * .25)] += 1
        world['carbon_dioxide_map'][int(world['world_size'] * .75)][int(world['world_size'] * .75)] += 1

        pr.place_plants(world)
        ps.photosynthesize(world)
        gd.move_gases(world['carbon_dioxide_map'], world['world_size'])
        ps.grow_plants(world)

        # TODO: Draw the world every 1000 frames.

    world['world_array'] = np.zeros(shape=(world['world_size'], world['world_size']), dtype=int)
    pr.place_plants(world)
