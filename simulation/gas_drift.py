import numpy as np
import numba as nb
from numba import prange
import scipy.sparse as sparse


@nb.jit(nopython=True, fastmath=True)
def move_gases(gas_map: np.array, world_size: int):
    gas_filled_squares = np.nonzero(gas_map)
    for parallel_index in range(len(gas_filled_squares[0])):
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


# @nb.jit(nopython=True, fastmath=True)
def move_gases_scipy_sparse_matrix(gas_map: sparse.csc_matrix, world_size: int):
    gas_filled_squares = gas_map.nonzero()
    row = np.array([])
    col = np.array([])
    data = np.array([])

    for parallel_index in range(len(gas_filled_squares[0])):
        x = gas_filled_squares[0][parallel_index]
        y = gas_filled_squares[1][parallel_index]
        possible_places_to_go = []
        gas_value = gas_map.getrow(x).getcol(y).data[0]

        if x > 0 and len(gas_map.getrow(x - 1).getcol(y).data) > 0 and gas_map.getrow(x - 1).getcol(y).data[0] < gas_value:
            possible_places_to_go.append((x - 1, y))
        else:
            if len(gas_map.getrow(x - 1).getcol(y).data) == 0:
                possible_places_to_go.append((x - 1, y))

        if x < world_size - 1 and len(gas_map.getrow(x + 1).getcol(y).data) > 0 and gas_map.getrow(x + 1).getcol(y).data[0] < gas_value:
            possible_places_to_go.append((x + 1, y))
        else:
            if len(gas_map.getrow(x + 1).getcol(y).data) == 0:
                possible_places_to_go.append((x + 1, y))


        if y > 0 and len(gas_map.getrow(x).getcol(y - 1).data) > 0 and gas_map.getrow(x).getcol(y - 1).data[0] < gas_value:
            possible_places_to_go.append((x, y - 1))
        else:
            if len(gas_map.getrow(x).getcol(y - 1).data) == 0:
                possible_places_to_go.append((x, y - 1))


        if y < world_size - 1 and len(gas_map.getrow(x).getcol(y + 1).data) > 0 and gas_map.getrow(x).getcol(y + 1).data[0] < gas_value:
            possible_places_to_go.append((x, y + 1))
        else:
            if len(gas_map.getrow(x).getcol(y + 1).data) == 0:
                possible_places_to_go.append((x, y + 1))

        if len(possible_places_to_go) > 0:
            i, j = possible_places_to_go[np.random.randint(0, len(possible_places_to_go))]
            row = np.append(row, x)
            col = np.append(col, y)
            data = np.append(data, -1)

            row = np.append(row, i)
            col = np.append(col, j)
            data = np.append(data, 1)

            # gas_map[x][y] -= 1
            # gas_map[i][j] += 1

    modifications_matrix = sparse.coo_matrix((data, (row, col)), shape=(world_size, world_size))

    gas_map = gas_map + modifications_matrix
