import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns


# TODO: Add rendering caller to pass in a color and a world, with a key to use for the intensity such as age.
# Will need basically a reduce function over the plant list to get more interesting features.
def render_array(l: np.ndarray, title):
    fig1 = plt.figure(figsize=(20, 20))
    ax4 = fig1.add_subplot(122)
    ax4.title.set_text(title)
    ax4.imshow(l, interpolation='nearest', cmap=cm.Greens)
    plt.show()
    plt.close(fig1)


def display_world(world_dictionary):
    fig, axs = plt.subplots(2, 2)

    axs[0,0].title.set_text('Plant Locations')
    axs[0,0].imshow(world_dictionary['plant_location_array'], interpolation='nearest', cmap=cm.Greens)

    axs[1,0].title.set_text("Carbon Dioxide")
    axs[1,0].imshow(world_dictionary['carbon_dioxide_map'], interpolation='nearest', cmap=cm.Greys)

    axs[0,1].title.set_text("Land")
    axs[0,1].imshow(world_dictionary['land_array'], interpolation='nearest', cmap=cm.Oranges)

    axs[1,1].title.set_text("Water")
    axs[1,1].imshow(world_dictionary['water_array'], interpolation='nearest', cmap=cm.Blues)

    fig.tight_layout()
    plt.show()


def save_drawing_of_array(l: np.ndarray, title):
    fig3 = plt.gcf()
    ax4 = fig3.add_subplot(122)
    ax4.title.set_text(title)
    ax4.imshow(l, interpolation='nearest', cmap=cm.Greens)
    fig3.set_size_inches(18.5, 10.5)
    fig3.savefig('test2png.png', dpi=100)
    plt.close(fig3)
