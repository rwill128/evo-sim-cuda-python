import numpy as np

from plants.plant_rendering import PLANT_SEGMENT_DEAD

ENERGY_COST_FOR_PLANTS_PER_FRAME = 1

ENERGY_GAINED_FROM_ONE_CARBON_DIOXIDE = 100

ENERGY_AFTER_ADDING_BRANCH = 4000
ENERGY_NEEDED_TO_ADD_BRANCH = 5000


def grow_plants(world_params):
    for index, plant in enumerate(world_params['plants']):
        plant['age'] += 1
        if plant['energy'] > 0:
            plant['energy'] -= ENERGY_COST_FOR_PLANTS_PER_FRAME
        if plant['energy'] == 0:
            if len(plant['segments']) == 1:
                # Mark only segment dead
                plant['segments'][0][0] = PLANT_SEGMENT_DEAD
            else:
                # Mark random segment dead
                plant['segments'][np.random.randint(0, len(plant['segments']) - 1)][0] = PLANT_SEGMENT_DEAD

    new_growth = []

    for index, plant in enumerate(world_params['plants']):
        if plant['energy'] > ENERGY_NEEDED_TO_ADD_BRANCH:
            if plant['age'] > plant['fertile_age']:
                pass
            else:
                plant['energy'] = ENERGY_AFTER_ADDING_BRANCH
                joined_seg = plant['segments'][
                    np.random.randint(0, len(plant['segments'] - 1))]  # TODO: Should only grow off of live segments
                new_seg = [
                    1,
                    joined_seg[3],
                    joined_seg[4],
                    joined_seg[3] + np.random.randint(-1, 1),
                    joined_seg[4] + np.random.randint(-1, 1)]
                new_growth.append((index, new_seg))

    for index, new_segment in new_growth:
        world_params['plants'][index]['segments'] = np.append(world_params['plants'][index]['segments'], [new_segment], 0)


def photosynthesize(world_params):
    occupied_squares = np.nonzero(world_params['world_array'])
    for index, x in enumerate(occupied_squares[0]):
        y = occupied_squares[1][index]
        if world_params['carbon_dioxide_map'][x][y] > 0:
            world_params['carbon_dioxide_map'][x][y] -= 1
            world_params['plants'][pull_plant_id_from_world(world_params, x, y) - 1][
                'energy'] += ENERGY_GAINED_FROM_ONE_CARBON_DIOXIDE


def pull_plant_id_from_world(world_params, x, y):
    return int(np.round(world_params['world_array'][x][y]))
