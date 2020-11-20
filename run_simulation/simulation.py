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


def run_sim_for_x_steps(world_dict, steps):
    emitters = [create_emitter(world_dict) for i in range(8)]

    for i in range(steps):
        gd.emit_gases(world_dict, emitters)
        ps.photosynthesize(world_dict['carbon_dioxide_map'],
                           world_dict['alive_plant_ids'],
                           world_dict['alive_plant_energy'],
                           world_dict['alive_plant_energy_gained_from_one_carbon_dioxide'],
                           world_params=world_dict)
        gd.move_gases(world_dict['carbon_dioxide_map'])
        ps.grow_plants(world_dict)

        if i % 1000 == 0:
            ar.save_drawing_of_world(world_params=world_dict, i=i)
