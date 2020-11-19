import numpy as np

from plants.plant_creation import generate_random_seedling
from plants.plant_rendering import PLANT_SEGMENT_DEAD, detect_occluded_squares, clear_occluded_square


def grow_plants(world_params):
    world_params['alive_plant_ages'] += 1
    world_params['alive_plant_energy'] = world_params['alive_plant_energy'] - (world_params['num_alive_segments'] * world_params['energy_cost_per_frame'])
    for index, plant in enumerate(world_params['plants']):
        if world_params['alive_plant_energy'][index] <= 0:
            if world_params['num_alive_segments'][index] == 1:
                # Mark only segment dead
                only_segment = plant['segments'][0]
                clear_occluded_square(l=only_segment[1:],
                                      x_translation=plant['x_translation'],
                                      y_translation=plant['y_translation'],
                                      c_id=plant['c_id'],
                                      plant_location_array=world_params['plant_location_array'],
                                      occupied_squares=world_params['occupied_squares'])
                only_segment[0] = PLANT_SEGMENT_DEAD
                plant['segments'] = np.delete(plant['segments'], 0, 0)
                plant['dead_segments'].append(only_segment)
                world_params['num_alive_segments'][index] = 0
            else:
                # Mark random segment dead
                segment_to_kill_index = np.random.randint(0, world_params['num_alive_segments'][index])
                segment_to_kill = plant['segments'][segment_to_kill_index]
                clear_occluded_square(l=segment_to_kill[1:],
                                      x_translation=plant['x_translation'],
                                      y_translation=plant['y_translation'],
                                      c_id=plant['c_id'],
                                      plant_location_array=world_params['plant_location_array'],
                                      occupied_squares=world_params['occupied_squares'])
                segment_to_kill[0] = PLANT_SEGMENT_DEAD
                plant['segments'] = np.delete(plant['segments'], segment_to_kill_index, 0)
                plant['dead_segments'].append(segment_to_kill)
                world_params['num_alive_segments'][index] -= 1

            if world_params['num_alive_segments'][index] == 0:
                world_params['plants'].pop(index)

                world_params['alive_plant_ids'] = np.delete(world_params['alive_plant_ids'], index, 0)
                world_params['alive_plant_x_translation'] = np.delete(world_params['alive_plant_x_translation'], index, 0)
                world_params['alive_plant_y_translation'] = np.delete(world_params['alive_plant_y_translation'], index, 0)
                world_params['alive_plant_energy'] = np.delete(world_params['alive_plant_energy'], index, 0)
                world_params['alive_plant_ages'] = np.delete(world_params['alive_plant_ages'], index, 0)
                world_params['alive_plant_fertile_ages'] = np.delete(world_params['alive_plant_fertile_ages'], index, 0)
                world_params['alive_plant_energy_gained_from_one_carbon_dioxide'] = np.delete(world_params['alive_plant_energy_gained_from_one_carbon_dioxide'], index, 0)
                world_params['energy_cost_for_growth'] = np.delete(world_params['energy_cost_for_growth'], index, 0)
                world_params['throw_distance'] = np.delete(world_params['throw_distance'], index, 0)
                world_params['energy_floor_for_growth'] = np.delete(world_params['energy_floor_for_growth'], index, 0)
                world_params['energy_cost_per_frame'] = np.delete(world_params['energy_cost_per_frame'], index, 0)
                world_params['motherhood_cost'] = np.delete(world_params['motherhood_cost'], index, 0)
                world_params['num_alive_segments'] = np.delete(world_params['num_alive_segments'], index, 0)

                world_params['dead_plants'].append(plant)

    new_growth = []
    for index, plant in enumerate(world_params['plants']):
        if world_params['alive_plant_ages'][index] > world_params['alive_plant_fertile_ages'][index] and world_params['alive_plant_energy'][index] > world_params['motherhood_cost'][index]:
            seedling, seedling_id = generate_random_seedling(1, world_params, (plant['x_translation'], plant['y_translation']), plant, index)
            world_params['all_plants_dictionary'][seedling_id] = seedling
            world_params['plants'].append(seedling)
        if world_params['alive_plant_energy'][index] > world_params['energy_floor_for_growth'][index] and world_params['alive_plant_ages'][index] < world_params['alive_plant_fertile_ages'][index]:
            world_params['alive_plant_energy'][index] -= world_params['energy_cost_for_growth'][index]
            joined_seg = plant['segments'][np.random.randint(0, world_params['num_alive_segments'][index])]  # TODO: Should only grow off of live segments
            new_seg = [
                1,
                joined_seg[3],
                joined_seg[4],
                joined_seg[3] + np.random.choice([-1, 0, 1]),
                joined_seg[4] + np.random.choice([-1, 0, 1])]
            detect_occluded_squares(l=joined_seg[1:],
                                    x_translation=plant['x_translation'],
                                    y_translation=plant['y_translation'],
                                    c_id=plant['c_id'],
                                    plant_location_array=world_params['plant_location_array'],
                                    occupied_squares=world_params['occupied_squares'])
            new_growth.append((index, new_seg))

    for index, new_segment in new_growth:
        world_params['num_alive_segments'][index] += 1
        world_params['plants'][index]['segments'] = np.append(world_params['plants'][index]['segments'], [new_segment], 0)


def photosynthesize(carbon_dioxide_map, occupied_squares, plant_ids, plant_energies,
                    energy_gained_from_one_carbon_dioxide_values):
    for x, y, c_id in occupied_squares:
        if carbon_dioxide_map[x][y] > 0:
            carbon_dioxide_map[x][y] -= 1
            plant_index = np.where(plant_ids == c_id)[0][0]
            plant_energies[plant_index] += energy_gained_from_one_carbon_dioxide_values[plant_index]
