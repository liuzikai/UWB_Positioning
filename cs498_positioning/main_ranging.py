import numpy as np
import telnetlib
import threading
from datetime import datetime
import time

from data_io import *

dist_data = {}
dist_lock = threading.Lock()


def process_info_to_range(info):

    dist = {}
    rough_split = info.split('[')
    if len(rough_split) <= 2:
        return None
    dis_list = rough_split[1].split(']')[0].split(',')
    if len(dis_list) != 1:
        return None
    id_list = rough_split[2].split(']')[0].split(',')
    if len(id_list) != 1:
        return None
    if (len(dis_list) != len(id_list)) | (len(dis_list) != 1):
        return None

    for i in range(0, len(dis_list)):
        id_list[i] = id_list[i].strip('"')
        if id_list[i] in ref_nodes:
            dist[id_list[i]] = float(dis_list[i].strip('"'))

    if len(dist) != 1:
        return None

    return dist


if __name__ == '__main__':

    time_stamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    tn = telnetlib.Telnet(host="127.0.0.1", port=19021)
    tn.read_until("")  # clean up buffer
    raw_data_file = open("data/rng_%s_raw_data.txt" % time_stamp, "w", buffering=1)  # write to file immediately
    data_file_open("data/rng_%s.csv" % time_stamp, input("Please input comment for data file: "))

    while True:
        raw_data = tn.read_until('\n'.encode())
        data = raw_data.decode(errors='ignore')

        raw_data_file.write(data)
        # print(data)

        dist = process_info_to_range(data)
        if dist is not None:
            print(dist)
            write_point([dist["1818"]])

    data_file_close()
    raw_data_file.close()
    tn.close()
