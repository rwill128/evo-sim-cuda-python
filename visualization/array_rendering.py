import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def render_array(l: np.ndarray):
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(122)
    ax4.imshow(l, interpolation='nearest', cmap=cm.Greens)
    plt.show()


def display_world(world_params):
    fig: object = plt.figure()
    fig.suptitle('The World')

    plant_im = fig.add_subplot(122)
    plant_im.title.set_text("Plants")
    plant_im.imshow(world_params['world_array'], interpolation='nearest', cmap=cm.Greens)

    ax4 = fig.add_subplot(122)
    ax4.title.set_text("Carbon Dioxide")
    ax4.imshow(world_params['carbon_dioxide_map'], interpolation='nearest', cmap=cm.Greens)

    plt.show()
