import numpy as np
import numba as nb
from numba import prange


@nb.jit(nopython=True, fastmath=True, parallel=True)
def move_gases(gas_map: np.array, world_size: int):

    gas_filled_squares = np.nonzero(gas_map)
    for parallel_index in prange(len(gas_filled_squares[0])):
        x = gas_filled_squares[0][parallel_index]
        y = gas_filled_squares[1][parallel_index]
        possible_places_to_go = []
        gas_value = gas_map[x][y]
        if x > 0 and gas_map[x - 1][y] < gas_value:
            possible_places_to_go.append((x - 1, y))
        if x < world_size - 1 and gas_map[x + 1][y] < gas_value:
            possible_places_to_go.append((x + 1, y))
        if y > 0 and gas_map[x][y - 1] < gas_value:
            possible_places_to_go.append((x, y - 1))
        if y < world_size - 1 and gas_map[x][y + 1] < gas_value:
            possible_places_to_go.append((x, y + 1))

        if len(possible_places_to_go) > 0:
            i, j = possible_places_to_go[np.random.randint(0, len(possible_places_to_go))]
            gas_map[x][y] -= 1
            gas_map[i][j] += 1
