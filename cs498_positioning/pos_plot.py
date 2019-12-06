import numpy as np
import itertools
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from config import *

# Initialize figure
fig = plt.figure()
ax = Axes3D(fig)

# Pre-process reference nodes and cube
ref_points = np.column_stack(ref_nodes.values())
ref_coor_m = [np.min(ref_points, axis=1), np.max(ref_points, axis=1)]

# Setup figure
ax.set_xlim3d(ref_coor_m[0][0] - plot_margin, ref_coor_m[1][0] + plot_margin)
ax.set_ylim3d(ref_coor_m[0][1] - plot_margin, ref_coor_m[1][1] + plot_margin)
ax.set_zlim3d(ref_coor_m[0][2] - plot_margin, ref_coor_m[1][2] + plot_margin)


def plot_ref_nodes():
    """
    Plot reference nodes and a minimal box that enclose all reference nodes
    :return: None
    """
    print(ref_points[0])
    ax.scatter(ref_points[0], ref_points[1], ref_points[2], c='b', s=80, marker='*')
    for m in itertools.product([0, 1], repeat=2):  # min(0) max(1) combinations
        print(m)
        # X min to max
        ax.plot([ref_coor_m[0][0], ref_coor_m[1][0]],
                [ref_coor_m[m[0]][1], ref_coor_m[m[0]][1]],
                [ref_coor_m[m[1]][2], ref_coor_m[m[1]][2]], c='c')
        # Y min to max
        ax.plot([ref_coor_m[m[0]][0], ref_coor_m[m[0]][0]],
                [ref_coor_m[0][1], ref_coor_m[1][1]],
                [ref_coor_m[m[1]][2], ref_coor_m[m[1]][2]], c='c')
        # Z min to max
        ax.plot([ref_coor_m[m[0]][0], ref_coor_m[m[0]][0]],
                [ref_coor_m[m[1]][1], ref_coor_m[m[1]][1]],
                [ref_coor_m[0][2], ref_coor_m[1][2]], c='c')


def plot_point(coor, c='r', marker='*'):
    """
    Plot a single point
    :param coor: 1D np.array of [x, y, z]
    :param c: color passes to plot()
    :param marker: marker passes to plot()
    :return: None
    """
    ax.plot([coor[0]], [coor[1]], [coor[2]], c=c, marker=marker)


def plot_points(points, c='r', marker='*'):
    """
    Plot multiple points
    :param points: 2D np.array with points as columns
    :param c: color passes to plot()
    :param marker: marker passes to plot()
    :return: None
    """
    ax.plot(points[0], points[1], points[2], c=c, marker=marker)


def plot_clear():
    plt.clf()


if __name__ == '__main__':
    plot_ref_nodes()
    plot_point(np.array([1.85137162, 3.62393441, -0.06691707]))
    plot_point(np.array([3.85137162, 1.62393441, 1.06691707]))
    plt.show()



