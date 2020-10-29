import numpy as np
import creature_spawning.spawn_creature as sc
import visualization.plant_rendering as pr
import visualization.array_rendering as ar
import simulation.gas_drift as gd
import simulation.plant_simulation as ps


def run_sim_for_x_steps(world, steps):
    for i in range(steps):
        world['world_array'] = np.zeros(shape=(world['world_size'], world['world_size']), dtype=int)
        world['carbon_dioxide_map'][int(world['world_size'] * .25)][int(world['world_size'] * .25)] += 1
        world['carbon_dioxide_map'][int(world['world_size'] * .25)][int(world['world_size'] * .75)] += 1
        world['carbon_dioxide_map'][int(world['world_size'] * .75)][int(world['world_size'] * .25)] += 1
        world['carbon_dioxide_map'][int(world['world_size'] * .75)][int(world['world_size'] * .75)] += 1

        pr.place_plants(world)
        ps.photosynthesize(world)
        gd.move_gases(world['carbon_dioxide_map'], world['world_size'])
        ps.grow_plants(world)

    world['world_array'] = np.zeros(shape=(world['world_size'], world['world_size']), dtype=int)
    pr.place_plants(world)