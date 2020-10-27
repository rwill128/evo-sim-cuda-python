import numpy as np


def move_gases(world_params):
    gas_filled_squares = np.nonzero(world_params['carbon_dioxide_map'])
    for index, x in enumerate(gas_filled_squares[0]):
        y = gas_filled_squares[1][index]
        possible_places_to_go = []
        gas_value = world_params['carbon_dioxide_map'][x][y]
        if x > 0 and world_params['carbon_dioxide_map'][x - 1][y] < gas_value:
            possible_places_to_go.append((x - 1, y))
        if x < world_params['world_size'] - 1 and world_params['carbon_dioxide_map'][x + 1][y] < gas_value:
            possible_places_to_go.append((x + 1, y))
        if y > 0 and world_params['carbon_dioxide_map'][x][y - 1] < gas_value:
            possible_places_to_go.append((x, y - 1))
        if y < world_params['world_size'] - 1 and world_params['carbon_dioxide_map'][x][y + 1] < gas_value:
            possible_places_to_go.append((x, y + 1))

        if len(possible_places_to_go) > 0:
            i, j = possible_places_to_go[np.random.randint(0, len(possible_places_to_go)) - 1]
            world_params['carbon_dioxide_map'][x][y] -= 1
            world_params['carbon_dioxide_map'][i][j] += 1
