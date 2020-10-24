import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def render_array(l: np.ndarray):
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(122)
    ax4.imshow(l, interpolation='nearest', cmap=cm.Greens)
    plt.show()
