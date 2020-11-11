import numpy as np
import plants.plant_rendering as pr
import gases.gas_drift as gd
import plants.plant_simulation as ps
import visualization.array_rendering as ar
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def run_sim_for_x_steps(world, steps):
    emitter1 = {
        'x': int(world['world_size'] * .25),
        'y': int(world['world_size'] * .25),
        'vx': np.random.choice([-1, 1]),
        'vy': np.random.choice([-1, 1])
    }
    emitter2 = {
        'x': int(world['world_size'] * .25),
        'y': int(world['world_size'] * .75),
        'vx': np.random.choice([-1, 1]),
        'vy': np.random.choice([-1, 1])
    }
    emitter3 = {
        'x': int(world['world_size'] * .75),
        'y': int(world['world_size'] * .25),
        'vx': np.random.choice([-1, 1]),
        'vy': np.random.choice([-1, 1])
    }
    emitter4 = {
        'x': int(world['world_size'] * .75),
        'y': int(world['world_size'] * .75),
        'vx': np.random.choice([-1, 1]),
        'vy': np.random.choice([-1, 1])
    }

    emitters = [emitter1, emitter2, emitter3, emitter4]

    for i in range(steps):
        world['plant_location_array'] = np.zeros(shape=(world['world_size'], world['world_size']), dtype=int)

        gd.emit_gases(world, emitters)

        pr.place_plants(world)
        ps.photosynthesize(world)
        gd.move_gases(world['carbon_dioxide_map'], world['world_size'])
        ps.grow_plants(world)

        # TODO: Draw the world every 1000 frames.
        if i % 1000 == 0:
            ar.save_drawing_of_world(world, i)

            # Collect Stats
            world['plant_surface_area_history']['time'].append(i)
            world['plant_surface_area_history']['plant_surface_area_history'].append(
                np.count_nonzero(world['plant_location_array']))
            world['carbon_dioxide_amount_history']['time'].append(i)
            world['carbon_dioxide_amount_history']['carbon_dioxide_amount_history'].append(
                np.count_nonzero(world['carbon_dioxide_map']))

        if i == steps - 1:
            # Print final stats image.
            fig, axs = plt.subplots(1, 2)

            axs[0].plot(world['plant_surface_area_history']['time'],
                        world['plant_surface_area_history']['plant_surface_area_history'])
            axs[0].set(xlabel='Time (i)', ylabel='Plant Surface Area',
                       title='Plant Surface Area')
            axs[0].grid()

            axs[1].plot(world['carbon_dioxide_amount_history']['time'],
                        world['carbon_dioxide_amount_history']['carbon_dioxide_amount_history'])
            axs[1].set(xlabel='Time (i)', ylabel='Carbon Dioxide Amount',
                       title='Carbon Dioxide Amount')
            axs[1].grid()

            fig.savefig("/tmp/build-artifacts/history.png")
            plt.close()
