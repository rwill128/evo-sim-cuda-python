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


# TODO: Actually, use another visualization library
# https://seaborn.pydata.org/
# https://holoviews.org/
# http://ggplot.yhathq.com/
def display_world(world_params):
    fig, axs = plt.subplots(1, 2)

    axs[0].title.set_text('World')
    axs[0].imshow(world_params['world_array'], interpolation='nearest', cmap=cm.Greens)

    axs[1].title.set_text("Carbon Dioxide")
    axs[1].imshow(world_params['carbon_dioxide_map'], interpolation='nearest', cmap=cm.Greens)

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
