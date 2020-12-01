import numpy as np
import gases.gas_drift as gd
import plants.plant_simulation as ps
import visualization.array_rendering as ar
from pathlib import Path
import pickle


def create_emitter(world):
    emitter = {
        'x': np.random.randint(10, world['world_size'] - 10),
        'y': np.random.randint(10, world['world_size'] - 10),
        'vx': np.random.choice([-1, 1]),
        'vy': np.random.choice([-1, 1])
    }
    return emitter


def run_sim_for_x_steps(world_params, steps):
    emitters = [create_emitter(world_params) for i in range(50)]

    for i in range(steps):
        gd.emit_gases(world_params, emitters)
        ps.photosynthesize(plant_location_array=world_params['plant_location_array'],
                           carbon_dioxide_map=world_params['carbon_dioxide_map'],
                           plant_ids=world_params['plant_ids'],
                           plant_energy=world_params['plant_energy'],
                           energy_gained_from_one_carbon_dioxide=world_params['energy_gained_from_one_carbon_dioxide'])
        gd.move_gases(world_params['carbon_dioxide_map'])
        ps.grow_plants(world_params)

        if i % 1000 == 0:
            ar.save_drawing_of_world(world_params=world_params, i=i)

            # Save game:
            save_path = Path('C:\evo-sim-records\saves\game_state.obj')
            save_file = save_path.open(mode='wb')
            pickle.dump(world_params, save_file)
            save_file.close()

