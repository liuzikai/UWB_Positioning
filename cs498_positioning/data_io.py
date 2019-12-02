import numpy as np
from config import *

"""
Data file format: 3 columns CSV

Part 1: Comments,len(ref_nodes),
Part 2: ref_node_x,ref_node_y,ref_node_z
Part 3: pos_x,pos_y,pos_z
"""

data_file = None


def data_file_open(filename, comment=""):
    global data_file

    if data_file is not None:
        print("There is already a data file opened")
        return

    data_file = open(filename, "w", buffering=1)  # write to file immediately

    data_file.write("%s,%d," % (comment, len(ref_nodes)) + "\n")

    for n in ref_nodes.values():
        data_file.write(",".join(str(x) for x in list(n)) + "\n")


def data_file_close():
    global data_file

    if data_file is None:
        print("No data file opened")
        return

    data_file.close()
    data_file = None


def write_point(coor):
    """
    Write a position to data file
    :param coor: list or 1D np.array of [x, y, z]
    :return: None
    """
    data_file.write(",".join(str(x) for x in list(coor)) + "\n")


def read_data(filename):

    """
    Read positioning data set from a file
    :param filename:
    :return: (comment, 2D np.array with columns of positions)
    """

    global ref_nodes

    ref_nodes = {}
    pos_list = []
    with open(filename, "r") as file:
        comment, ref_count, _ = tuple(file.readline()[:-1].split(","))  # eliminate '/n'
        ref_count = int(ref_count)
        for i in range(ref_count):
            ref_nodes[str(i)] = np.array([float(x) for x in file.readline()[:-1].split(",")])  # eliminate '/n'
        for line in file:
            pos_list.append(np.array([float(x) for x in line[:-1].split(",")]))  # eliminate '/n'
    return comment, np.column_stack(pos_list)


if __name__ == '__main__':
    data_file_open("data_file_test.csv", "Test data file")
    write_point(np.array([1, 2, 3]))
    write_point(np.array([4, 5, 6]))
    write_point(np.array([7, 8, 9]))
    data_file_close()

    ref_nodes = []  # clear ref_nodes for test

    file_comment, points = read_data("data/data_file_test.csv")
    print(file_comment)
    print(ref_nodes)
    print(points)
