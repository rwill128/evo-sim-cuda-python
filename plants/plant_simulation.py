import numpy as np
from numba import njit

from plants.plant_creation import generate_random_seedling
from plants.plant_rendering import PLANT_SEGMENT_DEAD, detect_occluded_squares, clear_occluded_square


def grow_plants(world_params):
    array_based_grow_plants(world_params)
    array_based_kill_plants(world_params)

    no_energy_indexes = np.where(world_params['plant_energy'] <= 0)[0]
    if len(no_energy_indexes) > 0:
        for index in no_energy_indexes:
            plant = world_params['plants'][index]
            if world_params['plant_energy'][index] <= 0:
                if world_params['num_alive_segments'][index] == 1:
                    # Mark only segment dead
                    segment = plant['segments'][0]
                    clear_occluded_square(segment[1], segment[2], segment[3], segment[4],
                                          x_translation=world_params['x_translation'][index],
                                          y_translation=world_params['y_translation'][index],
                                          plant_location_array=world_params['plant_location_array'])
                    segment[0] = PLANT_SEGMENT_DEAD
                    plant['segments'] = np.delete(plant['segments'], 0, 0)
                    world_params['num_alive_segments'][index] = 0
                if world_params['num_alive_segments'][index] > 1:
                    # Mark random segment dead
                    segment_to_kill_index = np.random.randint(0, world_params['num_alive_segments'][index])
                    segment_to_kill = plant['segments'][segment_to_kill_index]
                    clear_occluded_square(segment_to_kill[1], segment_to_kill[2], segment_to_kill[3], segment_to_kill[4],
                                          x_translation=world_params['x_translation'][index],
                                          y_translation=world_params['y_translation'][index],
                                          plant_location_array=world_params['plant_location_array'])
                    segment_to_kill[0] = PLANT_SEGMENT_DEAD
                    plant['segments'] = np.delete(plant['segments'], segment_to_kill_index, 0)
                    world_params['num_alive_segments'][index] -= 1

    for index, plant_id in enumerate(world_params['plant_ids']):
        plant = world_params['plants'][index]
        if world_params['plant_energy'][index] > world_params['energy_floor_for_growth'][index] and world_params['alive_plant_ages'][index] < world_params['fertile_age'][index] and world_params['num_alive_segments'][index] > 1:
            if len(plant['segments']) == 0:
                only_segment = [
                    1,
                    0,
                    0,
                    np.random.choice([-1, 0, 1]),
                    np.random.choice([-1, 0, 1])]
                detect_occluded_squares(only_segment[1], only_segment[2], only_segment[3], only_segment[4],
                                        x_translation=world_params['x_translation'][index],
                                        y_translation=world_params['y_translation'][index],
                                        c_id=world_params['plant_ids'][index],
                                        plant_location_array=world_params['plant_location_array'])
                world_params['num_alive_segments'][index] += 1
                world_params['plants'][index]['segments'] = np.append(world_params['plants'][index]['segments'], [only_segment], 0)
            else:
                if len(plant['segments']) == 1:
                    joined_seg = plant['segments'][0]
                else:
                    joined_seg = plant['segments'][np.random.randint(0, world_params['num_alive_segments'][index])]  # TODO: Should only grow off of live segments
                new_seg = [
                    1,
                    joined_seg[3],
                    joined_seg[4],
                    joined_seg[3] + np.random.choice([-1, 0, 1]),
                    joined_seg[4] + np.random.choice([-1, 0, 1])]
                detect_occluded_squares(joined_seg[1], joined_seg[2], joined_seg[3], joined_seg[4],
                                        x_translation=world_params['x_translation'][index],
                                        y_translation=world_params['y_translation'][index],
                                        c_id=world_params['plant_ids'][index],
                                        plant_location_array=world_params['plant_location_array'])
                world_params['num_alive_segments'][index] += 1
                world_params['plants'][index]['segments'] = np.append(world_params['plants'][index]['segments'], [new_seg], 0)


    indexes_where_plants_have_reached_fertile_age = np.where(
        np.greater(world_params['alive_plant_ages'], world_params['fertile_age']) == True)
    indexes_where_plants_have_enough_energy_for_motherhood_cost = np.where(
        np.greater(world_params['plant_energy'], world_params['motherhood_cost']) == True)
    reproduction_indexes = np.intersect1d(indexes_where_plants_have_reached_fertile_age,
                                          indexes_where_plants_have_enough_energy_for_motherhood_cost)

    if len(reproduction_indexes) > 0:
        for index in reproduction_indexes:
            seedling, seedling_id = generate_random_seedling(world_params, (world_params['x_translation'][index], world_params['y_translation'][index]), index)
            world_params['plants'].append(seedling)


def array_based_grow_plants(world_params):
    world_params['alive_plant_ages'] += 1
    world_params['plant_energy'] = world_params['plant_energy'] - (
                world_params['num_alive_segments'] * world_params['energy_cost_per_frame'])


def array_based_kill_plants(world_params):
    no_energy = np.where(world_params['plant_energy'] <= 0)
    no_segments = np.where(world_params['num_alive_segments'] <= 0)
    dead_indexes = np.intersect1d(no_energy, no_segments)
    if len(dead_indexes) > 0:
        world_params['plant_ids'] = np.delete(world_params['plant_ids'], dead_indexes, 0)
        world_params['plant_energy'] = np.delete(world_params['plant_energy'], dead_indexes, 0)
        world_params['alive_plant_ages'] = np.delete(world_params['alive_plant_ages'], dead_indexes, 0)
        world_params['fertile_age'] = np.delete(world_params['fertile_age'], dead_indexes, 0)
        world_params['energy_gained_from_one_carbon_dioxide'] = np.delete(
            world_params['energy_gained_from_one_carbon_dioxide'], dead_indexes, 0)
        world_params['energy_cost_for_growth'] = np.delete(world_params['energy_cost_for_growth'], dead_indexes, 0)
        world_params['throw_distance'] = np.delete(world_params['throw_distance'], dead_indexes, 0)
        world_params['energy_floor_for_growth'] = np.delete(world_params['energy_floor_for_growth'], dead_indexes, 0)
        world_params['energy_cost_per_frame'] = np.delete(world_params['energy_cost_per_frame'], dead_indexes, 0)
        world_params['motherhood_cost'] = np.delete(world_params['motherhood_cost'], dead_indexes, 0)
        world_params['x_translation'] = np.delete(world_params['x_translation'], dead_indexes, 0)
        world_params['y_translation'] = np.delete(world_params['y_translation'], dead_indexes, 0)
        world_params['num_alive_segments'] = np.delete(world_params['num_alive_segments'], dead_indexes, 0)
    for index in dead_indexes[::-1]:
        del world_params['plants'][index]


def photosynthesize(plant_location_array, carbon_dioxide_map, plant_ids, plant_energy,
                    energy_gained_from_one_carbon_dioxide):
    boolean_mask_of_both_presence = accelerated_photosynthesis_one(carbon_dioxide_map, plant_location_array)

    carbon_dioxide_map[boolean_mask_of_both_presence] -= 1

    global_indices_of_plants_gaining_energy_this_frame = accelerated_where(
        np.in1d(plant_ids, plant_location_array[boolean_mask_of_both_presence]))

    plant_energy[global_indices_of_plants_gaining_energy_this_frame] = \
        plant_energy[global_indices_of_plants_gaining_energy_this_frame] \
        + energy_gained_from_one_carbon_dioxide[global_indices_of_plants_gaining_energy_this_frame]


def accelerated_where(in1d_var):
    frame = np.where(in1d_var)[0]
    return frame


@njit()
def accelerated_photosynthesis_one(carbon_dioxide_map, plant_location_array):
    return np.logical_and(plant_location_array, carbon_dioxide_map)
