import numpy as np
import numba as nb

from plants.plant_creation import generate_random_seedling
from plants.plant_rendering import PLANT_SEGMENT_DEAD

ENERGY_COST_FOR_PLANTS_PER_FRAME = 1

ENERGY_GAINED_FROM_ONE_CARBON_DIOXIDE: int = 100

ENERGY_AFTER_ADDING_BRANCH: int = 4000
ENERGY_AFTER_REPRODUCING: int = 4000
ENERGY_NEEDED_TO_ADD_BRANCH: int = 5000


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

            if np.count_nonzero(plant['segments'][:, 0]) == 0:
                world_params['plants'].pop(index)
                world_params['dead_plants'].append(plant)

    new_growth = []

    for index, plant in enumerate(world_params['plants']):
        if plant['energy'] > ENERGY_NEEDED_TO_ADD_BRANCH:
            if plant['age'] > plant['fertile_age']:
                plant['energy'] = ENERGY_AFTER_REPRODUCING
                seedling, seedling_id = generate_random_seedling(1, world_params)
                world_params['all_plants_dictionary'][seedling_id] = seedling
                world_params['plants'].append(seedling)
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
        world_params['plants'][index]['segments'] = np.append(world_params['plants'][index]['segments'], [new_segment],
                                                              0)


def photosynthesize(world_array: np.array, carbon_dioxide_map: np.array, all_plants_dictionary: np.array):
    plants_to_breathe: np.ndarray = np.empty(1, dtype=int)
    plants_to_breathe[0] = 0

    breathe(world_array, carbon_dioxide_map, plants_to_breathe)

    if len(plants_to_breathe) > 0 and plants_to_breathe[0] != 0:
        for plant_id in plants_to_breathe:
            all_plants_dictionary[plant_id]['energy'] += ENERGY_GAINED_FROM_ONE_CARBON_DIOXIDE


@nb.jit(nopython=True, fastmath=True)
def breathe(world_array: np.array, carbon_dioxide_map: np.array, plants_to_breathe: np.array):
    occupied_squares = np.nonzero(world_array)
    for index, x in enumerate(occupied_squares[0]):
        y = occupied_squares[1][index]
        if carbon_dioxide_map[x][y] > 0:
            carbon_dioxide_map[x][y] = carbon_dioxide_map[x][y]
            if plants_to_breathe[0] == 0:
                plants_to_breathe[0] = pull_plant_id_from_world(world_array, x, y)
            else:
                plants_to_breathe = np.append(plants_to_breathe, pull_plant_id_from_world(world_array, x, y))


@nb.jit(nopython=True, fastmath=True)
def pull_plant_id_from_world(world_array: np.array, x: int, y: int):
    return world_array[x][y]
