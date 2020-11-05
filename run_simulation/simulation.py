import numpy as np
import plants.plant_rendering as pr
import gases.gas_drift as gd
import plants.plant_simulation as ps
import visualization.array_rendering as ar


def run_sim_for_x_steps(world, steps):

    emitter1 = {
        'x': int(world['world_size'] * .25),
        'y': int(world['world_size'] * .25),
        'vx': np.random.randint(-1, 1),
        'vy': np.random.randint(-1, 1)
    }
    emitter2 = {
        'x': int(world['world_size'] * .25),
        'y': int(world['world_size'] * .75),
        'vx': np.random.randint(-1, 1),
        'vy': np.random.randint(-1, 1)
    }
    emitter3 = {
        'x': int(world['world_size'] * .75),
        'y': int(world['world_size'] * .25),
        'vx': np.random.randint(-1, 1),
        'vy': np.random.randint(-1, 1)
    }
    emitter4 = {
        'x': int(world['world_size'] * .75),
        'y': int(world['world_size'] * .75),
        'vx': np.random.randint(-1, 1),
        'vy': np.random.randint(-1, 1)
    }

    emitters = [emitter1, emitter2, emitter3, emitter4]

    for i in range(steps):
        world['world_array'] = np.zeros(shape=(world['world_size'], world['world_size']), dtype=int)

        gd.emit_gases(world, emitters)

        pr.place_plants(world)
        ps.photosynthesize(world)
        gd.move_gases(world['carbon_dioxide_map'], world['world_size'])
        ps.grow_plants(world)

        # TODO: Draw the world every 1000 frames.
        if i % 500 == 0:
            ar.render_array(world['world_array'], 'Plants')
            ar.render_array(world['carbon_dioxide_map'], 'Carbon Dioxide')