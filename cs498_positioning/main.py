import numpy as np
import telnetlib
import threading
from datetime import datetime
import time

from config import *
from positioning import *
from pos_plot import *
from kalman import *
from data_io import *

dist_data = {}
dist_lock = threading.Lock()


class DataThread(threading.Thread):
    def __init__(self, comment, input_data_file):
        threading.Thread.__init__(self)
        self.comment = comment
        self.input_data_file = input_data_file

    def run(self):

        global dist_data
        global dist_lock

        time_stamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        if self.input_data_file == "":  # collect and store data from telnet port
            tn = telnetlib.Telnet(host="127.0.0.1", port=19021)
            raw_data_file = open("data/%s_raw_data.txt" % time_stamp, "w", buffering=1)  # write to file immediately
            data_file_open("data/%s_pos.csv" % time_stamp, self.comment)
        else:  # re-process data from raw data file
            fin = open(self.input_data_file, "r")
            data_file_open("data/%s_reprocess_%s_pos.csv" %
                           (self.input_data_file.split("/")[-1].replace(".", "_"), time_stamp),
                           self.comment)
            time.sleep(1)  # wait for another thread to get started

        utime_init = None
        time_init = time.time()

        while True:

            if self.input_data_file == "":
                raw_data = tn.read_until('\n'.encode())
                data = raw_data.decode(errors='ignore')
                raw_data_file.write(data)
            else:
                data = fin.readline()
                if data is None:
                    break
                if data.startswith('{"utime": '):
                    utime = float(data[10:data.find(",")])
                    if utime_init is not None:
                        to_sleep = time_init + (utime - utime_init) / 6400000 - time.time()
                        # print(to_sleep)
                        if to_sleep > 0:
                            time.sleep(to_sleep)
                    else:
                        utime_init = utime

            # print(data)

            dist = process_info(data)
            if dist is None:
                continue
            # print(dist)

            with dist_lock:
                for k, v in dist.items():
                    if k not in dist_data.keys():
                        dist_data[k] = []
                    dist_data[k].append(v)

        data_file_close()
        if self.input_data_file == "":
            raw_data_file.close()
            tn.close()
        else:
            fin.close()


class PlotThread(threading.Thread):
    def __init__(self, disable_plot=False):
        threading.Thread.__init__(self)
        self.disable_plot = disable_plot

    def run(self):

        global dist_data, dist_lock

        if not self.disable_plot:
            plt.ion()
            plt.show()

        time_init = time.time()
        loop_counter = 0
        while True:

            if not self.disable_plot:
                plot_clear()
                plot_ref_nodes()

            dist = {}

            with dist_lock:
                for k, v in dist_data.items():
                    print(len(v))
                    filtered_dist = pre_process_data(v)
                    if filtered_dist is not None:
                        dist[k] = filtered_dist
                dist_data = {}

            if len(dist.keys()) >= 4:
                # print(dist)
                pos = calc_position(dist)
                if not self.disable_plot:
                    plot_point([pos[0], pos[1], pos[2]])
                write_point(pos)

                if not self.disable_plot:
                    plt.draw()
                    # plt.show()

            to_sleep = time_init + 1 * loop_counter - time.time()
            if to_sleep > 0:
                time.sleep(to_sleep)

            loop_counter += 1


if __name__ == '__main__':

    input_data_file = input("Input data file (relative path, empty for collecting data from telnet): ")

    data_thread = DataThread(input("Please input comment for data file: "), input_data_file)
    plot_thread = PlotThread(disable_plot=True)
    data_thread.start()
    plot_thread.start()
    data_thread.join()
    plot_thread.join()
