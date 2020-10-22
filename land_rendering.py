import matplotlib.pyplot as plt
import matplotlib.cm as cm


def render_land(l):
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(122)
    ax4.imshow(l, interpolation='nearest', cmap=cm.Greys_r)
    plt.show()
