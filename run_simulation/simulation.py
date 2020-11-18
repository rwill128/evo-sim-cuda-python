import numpy as np
import gases.gas_drift as gd
import plants.plant_simulation as ps
import visualization.array_rendering as ar


def create_emitter(world):
    emitter = {
        'x': np.random.randint(10, world['world_size'] - 10),
        'y': np.random.randint(10, world['world_size'] - 10),
        'vx': np.random.choice([-1, 1]),
        'vy': np.random.choice([-1, 1])
    }
    return emitter


def run_sim_for_x_steps(world_dict, world_array, steps):
    emitters = [create_emitter(world_dict) for i in range(8)]

    for i in range(steps):
        gd.emit_gases(world_dict, emitters)
        ps.photosynthesize(world_dict['carbon_dioxide_map'],
                           world_dict['all_plants_dictionary'],
                           world_dict['occupied_squares'])
        gd.move_gases(world_dict['carbon_dioxide_map'], world_dict['world_size'])
        ps.grow_plants(world_dict)

        if i % 100 == 0:
            ar.save_drawing_of_world(world_params=world_dict, i=i)
