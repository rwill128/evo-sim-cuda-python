import numpy as np
import plants.plant_rendering as pr
import gases.gas_drift as gd
import plants.plant_simulation as ps
import visualization.array_rendering as ar
import matplotlib.pyplot as plt

def create_emitter(world):
    emitter = {
        'x': np.random.randint(10, world['world_size'] - 10),
        'y': np.random.randint(10, world['world_size'] - 10),
        'vx': np.random.choice([-1, 1]),
        'vy': np.random.choice([-1, 1])
    }
    return emitter


def run_sim_for_x_steps(world_dict, world_array, steps):

    emitters = [create_emitter(world_dict) for emitter in range(400)]

    for i in range(steps):
        world_dict['plant_location_array'] = np.zeros(shape=(world_dict['world_size'], world_dict['world_size']), dtype=int)

        gd.emit_gases(world_dict, emitters)

        pr.place_plants(world_dict)
        ps.photosynthesize(world_dict)
        gd.move_gases(world_dict['carbon_dioxide_map'], world_dict['world_size'])
        ps.grow_plants(world_dict)