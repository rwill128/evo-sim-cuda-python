import math

import numpy as np
import numba as nb
from numba import prange
import scipy.sparse as sparse
import sys


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
    sys.setrecursionlimit(10000)
    gas_filled_squares = gas_map.nonzero()
    gas_values = sparse.csc_matrix(gas_map[gas_filled_squares]).toarray()

    row_test: np.array = np.array([])
    col_test: np.array = np.array([])
    data_test: np.array = np.array([])
    row_test, col_test, data_test = numba_move_gases(gas_filled_squares[0], gas_filled_squares[1], gas_values,
                                                     row_test.copy(), col_test.copy(),
                                                     data_test.copy(), world_size)

    modifications_matrix = sparse.coo_matrix((data_test, (row_test, col_test)), shape=(world_size, world_size)).tocsc()
    return gas_map + modifications_matrix


# @nb.jit(nopython=True, fastmath=True)
def numba_move_gases(x_squares: np.array, y_squares: np.array, gas_values: np.array, row_test: np.array,
                     col_test: np.array, data_test: np.array, world_size: int):
    for parallel_index in range(len(x_squares)):
        x = x_squares[parallel_index]
        y = y_squares[parallel_index]
        value = gas_values[0, parallel_index]

        row_test = np.append(row_test, x)
        col_test = np.append(col_test, y)
        data_test = np.append(data_test, -1)

        up = np.array([x, y + 1])
        down = np.array([x, y - 1])
        left = np.array([x - 1, y])
        right = np.array([x + 1, y])
        choice_mask = np.array([up, down, right, left])
        choices = np.random.choice(np.array([0, 1, 2, 3]), 4)

        for choice in choices:
            i, j = choice_mask[choice]
            if len(np.where(x_squares == i)[0]) == 0 or len(
                    np.where(y_squares[np.where(x_squares == i)[0]] == j)[0]) == 0:
                row_test = np.append(row_test, min(world_size - 1, max(0, i)))
                col_test = np.append(col_test, min(world_size - 1, max(0, j)))
                data_test = np.append(data_test, 1)
                break
            else:
                if gas_values[0, np.where(y_squares[np.where(x_squares == i)[0]] == j)[0][0]] < value:
                    row_test = np.append(row_test, min(world_size - 1, max(0, i)))
                    col_test = np.append(col_test, min(world_size - 1, max(0, j)))
                    data_test = np.append(data_test, 1)
                    break
    return row_test, col_test, data_test
