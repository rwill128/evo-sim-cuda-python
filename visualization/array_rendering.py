import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.cm as cm
import numpy as np


def render_array(l: np.ndarray, title):
    fig1 = plt.figure(figsize=(20, 20))
    ax4 = fig1.add_subplot(122)
    ax4.title.set_text(title)
    ax4.imshow(l, interpolation='nearest', cmap=cm.Greens)
    plt.show()
    plt.close(fig1)


def display_world(world_params):
    fig2: object = plt.figure()
    fig2.suptitle('The World')

    plant_im = fig2.add_subplot(122)
    plant_im.title.set_text("Plants")
    plant_im.imshow(world_params['world_array'], interpolation='nearest', cmap=cm.Greens)

    ax4 = fig2.add_subplot(122)
    ax4.title.set_text("Carbon Dioxide")
    ax4.imshow(world_params['carbon_dioxide_map'], interpolation='nearest', cmap=cm.Greens)

    plt.show()
    plt.close(fig2)


def save_drawing_of_array(l: np.ndarray, title):
    fig3 = plt.gcf()
    ax4 = fig3.add_subplot(122)
    ax4.title.set_text(title)
    ax4.imshow(l, interpolation='nearest', cmap=cm.Greens)
    fig3.set_size_inches(18.5, 10.5)
    fig3.savefig('test2png.png', dpi=100)
    plt.close(fig3)
