import numpy as np

from plants.plant_creation import generate_random_seedling
from plants.plant_rendering import PLANT_SEGMENT_DEAD, detect_occluded_squares, clear_occluded_square


def grow_plants(world_params):
    for index, plant in enumerate(world_params['plants']):
        plant['age'] += 1
        plant['num_alive_segments'] = len(plant['segments'])
        if plant['energy'] > 0:
            # TODO: each plant only loses one energy per frame no matter how many cells it has?
            plant['energy'] -= len(plant['segments'])
        if plant['energy'] <= 0:
            if len(plant['segments']) == 1:
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
            else:
                # Mark random segment dead
                segment_to_kill_index = np.random.randint(0, len(plant['segments']))
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

            if len(plant['segments']) == 0:
                world_params['plants'].pop(index)

                world_params['alive_plant_ids'] = np.delete(world_params['alive_plant_ids'], index, 0)
                world_params['alive_plant_x_translation'] = np.delete(world_params['alive_plant_x_translation'], index,
                                                                      0)
                world_params['alive_plant_y_translation'] = np.delete(world_params['alive_plant_y_translation'], index,
                                                                      0)
                world_params['alive_plant_energy'] = np.delete(world_params['alive_plant_energy'], index, 0)
                world_params['alive_plant_ages'] = np.delete(world_params['alive_plant_ages'], index, 0)
                world_params['alive_plant_fertile_ages'] = np.delete(world_params['alive_plant_fertile_ages'], index, 0)

                world_params['dead_plants'].append(plant)

    new_growth = []
    for index, plant in enumerate(world_params['plants']):
        if plant['age'] > plant['fertile_age'] and plant['energy'] > plant['motherhood_cost']:
            seedling, seedling_id = generate_random_seedling(1, world_params,
                                                             (plant['x_translation'], plant['y_translation']), plant)
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
        world_params['plants'][index]['segments'] = np.append(world_params['plants'][index]['segments'], [new_segment],
                                                              0)


def photosynthesize(carbon_dioxide_map, all_plants_dictionary, occupied_squares):
    for x, y, c_id in occupied_squares:
        if carbon_dioxide_map[x][y] > 0:
            carbon_dioxide_map[x][y] -= 1
            all_plants_dictionary[c_id][
                'energy'] += all_plants_dictionary[c_id]['energy_gained_from_one_carbon_dioxide']
