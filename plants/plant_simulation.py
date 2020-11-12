import numpy as np
import numba as nb

from plants.plant_creation import generate_random_seedling
from plants.plant_rendering import PLANT_SEGMENT_DEAD


def grow_plants(world_params):
    for index, plant in enumerate(world_params['plants']):
        plant['age'] += 1
        alive_segment_indexes = np.where(plant['segments'][:, 0] != 0)
        if plant['energy'] > 0:
            # TODO: each plant only loses one energy per frame no matter how many cells it has?
            plant['energy'] -= len(alive_segment_indexes[0])
        if plant['energy'] <= 0:
            if len(plant['segments']) == 1:
                # Mark only segment dead
                plant['segments'][0][0] = PLANT_SEGMENT_DEAD
            else:
                # Mark random segment dead
                segment_to_kill_index = np.random.choice(alive_segment_indexes[0])
                plant['segments'][segment_to_kill_index][0] = PLANT_SEGMENT_DEAD

            if np.count_nonzero(plant['segments'][:, 0]) == 0:
                world_params['plants'].pop(index)
                world_params['dead_plants'].append(plant)

    new_growth = []
    for index, plant in enumerate(world_params['plants']):
        if plant['age'] > plant['fertile_age'] and plant['energy'] > plant['motherhood_cost']:
            seedling, seedling_id = generate_random_seedling(1, world_params, (plant['x_translation'], plant['y_translation']), plant)
            world_params['all_plants_dictionary'][seedling_id] = seedling
            world_params['plants'].append(seedling)
        if plant['energy'] > plant['energy_floor_for_growth'] and plant['age'] < plant['fertile_age']:
            plant['energy'] -= plant['energy_cost_for_growth']
            joined_seg = plant['segments'][
                np.random.randint(0, len(plant['segments']))]  # TODO: Should only grow off of live segments
            new_seg = [
                1,
                joined_seg[3],
                joined_seg[4],
                joined_seg[3] + np.random.randint(-1, 1),
                joined_seg[4] + np.random.randint(-1, 1)]
            new_growth.append((index, new_seg))

    for index, new_segment in new_growth:
        world_params['plants'][index]['segments'] = np.append(world_params['plants'][index]['segments'], [new_segment],
                                                              0)


def photosynthesize(world_params):
    occupied_squares = get_occupied_squares(world_params['plant_location_array'])
    for index, x in enumerate(occupied_squares[0]):
        y = occupied_squares[1][index]
        if world_params['carbon_dioxide_map'][x][y] > 0:
            world_params['carbon_dioxide_map'][x][y] -= 1
            world_params['all_plants_dictionary'][pull_plant_id_from_world(world_params, x, y)][
                'energy'] += world_params['all_plants_dictionary'][pull_plant_id_from_world(world_params, x, y)]['energy_gained_from_one_carbon_dioxide']


@nb.jit(nopython=True)
def get_occupied_squares(plant_location_array: np.array):
    return np.nonzero(plant_location_array)


def pull_plant_id_from_world(world_params, x, y):
    return world_params['plant_location_array'][x][y]
