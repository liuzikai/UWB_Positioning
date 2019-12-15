import numpy as np
import statistics as stat
from config import *


def process_info(info):

    """
    Process a line of info from data source and extract distance
    :param info: a line of info. See below for format sample
    :return: directory of {node_id (str): distance}
    """

    dist = {}
    rough_split = info.split('[')
    if len(rough_split) <= 2:
        return None
    dis_list = rough_split[1].split(']')[0].split(',')
    if len(dis_list) < 4:
        return None
    id_list = rough_split[2].split(']')[0].split(',')
    if len(id_list) < 4:
        return None
    if (len(dis_list) != len(id_list)) | (len(dis_list) < 4):
        return None

    for i in range(0, len(dis_list)):
        id_list[i] = id_list[i].strip('"')
        if id_list[i] in ref_nodes:
            dist[id_list[i]] = float(dis_list[i].strip('"'))

    if len(dist) < 4:
        return None

    return dist


pre_process_threshold = 999


def pre_process_data(ranges):

    """
    Pre-process a list of ranges from one reference node and eliminate points that are away from the medium by
    pre_process_threshold
    :param ranges: a list of ranges
    :return average range after filtering
    """

    median = stat.median(ranges)
    s = 0  # sum
    c = 0  # count
    for r in ranges:
        if median - pre_process_threshold < r < median + pre_process_threshold:
            s += r
            c += 1
    if c == 0:
        return None
    else:
        return s / c


def calc_position(dist):

    """
    Calculate position based on distances to reference point
    :param dist: directory of {node_id (str): distance}
    :return: 1D np.array of position [x, y, z]
    """

    A = np.array([0, 0, 0])
    B = np.array([0])

    for i in dist.keys():
        if i == base_node:
            continue
        A = np.vstack((A, ref_nodes[i] - ref_nodes[base_node]))
        B = np.vstack(
            (B, dist[i] ** 2 - dist[base_node] ** 2 - np.dot(ref_nodes[i] ** 2 - ref_nodes[base_node] ** 2, np.array([1, 1, 1]))))

    A = A[1:len(dist)]
    B = B[1:len(dist)] * (-0.5)

    AT = np.transpose(A)
    B = np.dot(AT, B)
    rev = np.linalg.inv(np.dot(AT, A))
    pos = np.dot(rev, B)
    posT = np.transpose(pos)

    return posT[0]


if __name__ == '__main__':
    dist = process_info(
        '{"utime": 2157172559,"survey": {"seq": 26,"mask": 15,"nrngs": [{"mask": 14,"nrng": ["2.495","3.583","2.443"]},{"mask": 13,"nrng": ["1.613","5.014","3.034"]},{"mask": 11,"nrng": ["3.550","4.971","5.377"]},{"mask": 7,"nrng": ["4.971","3.018","5.377"]}]}}')
    if dist is not None:
        print(dist)
        pos = calc_position(dist)
        if pos is not None:
            print(pos)
        else:
            print("Fail to calculate position")
    else:
        print("Fail to process info")
