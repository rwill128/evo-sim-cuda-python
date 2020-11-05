import numpy as np
import numba as nb


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


def emit_gases(world, emitters):
    
    for emitter in emitters:
        world['carbon_dioxide_map'][emitter['x']][emitter['y']] += 1

        if emitter['x'] < 5 and emitter['vx'] < 0:
            emitter['vx'] = -emitter['vx']        
        if emitter['y'] < 5 and emitter['vy'] < 0:
            emitter['vy'] = -emitter['vy']

        if emitter['x'] > world['world_size'] and emitter['vx'] > 0:
            emitter['vx'] = -emitter['vx']
        if emitter['y'] > world['world_size'] and emitter['vy'] > 0:
            emitter['vy'] = -emitter['vy']

        emitter['x'] += emitter['vx']
        emitter['y'] += emitter['vy']