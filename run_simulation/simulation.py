import numpy as np
import plants.plant_rendering as pr
import gases.gas_drift as gd
import plants.plant_simulation as ps
import visualization.array_rendering as ar
import matplotlib.pyplot as plt

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
            world['rate_of_energy_consumption']['time'].append(i)
            world['rate_of_energy_consumption']['rate_of_energy_consumption'].append(len(world['plants']))

        if i == steps - 1:
            # Print final stats image.
            fig, axs = plt.subplots(2, 2)

            axs[0, 0].plot(world['plant_surface_area_history']['time'],
                        world['plant_surface_area_history']['plant_surface_area_history'])
            axs[0, 0].set(xlabel='Time (i)', ylabel='Plant Surface Area',
                       title='Plant Surface Area')
            axs[0, 0].grid()

            axs[0, 1].plot(world['carbon_dioxide_amount_history']['time'],
                        world['carbon_dioxide_amount_history']['carbon_dioxide_amount_history'])
            axs[0, 1].set(xlabel='Time (i)', ylabel='Carbon Dioxide Amount',
                       title='Carbon Dioxide Amount')
            axs[0, 1].grid()

            axs[1, 0].plot(world['rate_of_energy_consumption']['time'],
                        world['rate_of_energy_consumption']['rate_of_energy_consumption'])
            axs[1, 0].set(xlabel='Time (i)', ylabel='Burn rate of energy by plants',
                       title='Rate of Energy Burn')
            axs[1, 0].grid()

            axs[1, 1].plot(world['carbon_dioxide_amount_history']['time'],
                        [i * 50 for i in world['carbon_dioxide_amount_history']['carbon_dioxide_amount_history']])
            axs[1, 1].set(xlabel='Time (i)', ylabel='Available Free Energy',
                       title='Available Energy in System')
            axs[1, 1].grid()

            fig.set_size_inches(10, 10)
            fig.tight_layout()
            # fig.savefig("/tmp/build-artifacts/history.png")
            plt.show()
            plt.close()
