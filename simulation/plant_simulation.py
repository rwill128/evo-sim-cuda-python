import numpy as np


def grow_plants(world_params):
    new_growth = []
    for index, plant in enumerate(world_params['plants']):
        if plant[0][4] > 10:
            plant[0][4] = 0
            joined_seg = plant[np.random.randint(1, len(plant))]
            new_seg = [0, joined_seg[3], joined_seg[4], joined_seg[3] + np.random.randint(-1, 1), joined_seg[4] + np.random.randint(-1, 1)]
            new_growth.append((index, np.append(plant, [new_seg], 0)))

    for index, new_plant in new_growth:
        world_params['plants'][index] = new_plant


def photosynthesize(world_params):
    occupied_squares = np.nonzero(world_params['world_array'])
    for index, x in enumerate(occupied_squares[0]):
        y = occupied_squares[1][index]
        if world_params['carbon_dioxide_map'][x][y] > 0:
            world_params['carbon_dioxide_map'][x][y] -= 1
            world_params['plants'][int(np.round(world_params['world_array'][x][y])) - 1][0][4] += 1
