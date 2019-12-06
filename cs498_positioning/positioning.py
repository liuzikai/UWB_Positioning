import numpy as np
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
            dist[id_list[i]] = (float)(dis_list[i].strip('"'))

    if len(dist) < 4:
        return None

    return dist


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
        '{"utime": 1322787487,"nrng": {"seq": 193,"mask": 15,"rng": ["3.513","3.909","2.267","2.680"],"uid": ["1818","5632","3884","1665"]}}')
    if dist is not None:
        print(dist)
    else:
        print("Fail to process info")
    pos = calc_position(dist)
    if pos is not None:
        print(pos)
    else:
        print("Fail to calculate position")
