import numpy as np
import telnetlib
import threading
from datetime import datetime

from config import *
from positioning import *
from pos_plot import *
from kalman import *
from data_io import *

dist_sum = np.array([0.0, 0.0, 0.0])
pos_sum = np.array([0.0, 0.0, 0.0])
pos_count = 0
pos_lock = threading.Lock()


class DataThread(threading.Thread):
    def __init__(self, comment):
        threading.Thread.__init__(self)
        self.comment = comment

    def run(self):

        global dist_sum, pos_sum, pos_count, pos_lock

        tn = telnetlib.Telnet(host="127.0.0.1", port=19021)
        time_stamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        raw_data_file = open("data/%s_raw_data.txt" % time_stamp, "w", buffering=1)  # write to file immediately
        data_file_open("data/%s_pos.csv" % time_stamp, self.comment)

        while True:

            raw_data = tn.read_until('\n'.encode())
            data = raw_data.decode(errors='ignore')

            raw_data_file.write(data)
            print(raw_data)
            dist = process_info(data)
            if (dist is None):
                continue;
            pos = calc_position(dist)

            write_point(pos)

            with pos_lock:
                pos_sum += pos
                pos_count += 1

        data_file_close()
        raw_data_file.close()
        tn.close()


class PlotThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        global dist_sum, pos_sum, pos_count, pos_lock

        plt.ion()
        plt.show()

        while True:

            plot_clear()
            plot_ref_nodes()
            with pos_lock:
                if pos_count != 0:
                    plot_point([pos_sum[0] / pos_count, pos_sum[1] / pos_count, pos_sum[2] / pos_count])
                    print(pos_count)
                    print("(%.3f, %.3f, %.3f)" % (dist_sum[0] / pos_count, dist_sum[1] / pos_count, dist_sum[2] / pos_count))
                    pos_sum = np.array([0.0, 0.0, 0.0])
                    pos_count = 0

            plt.draw()
            # plt.show()
            plt.pause(0.1)


if __name__ == '__main__':
    data_thread = DataThread(input("Please input comment for data file: "))
    plot_thread = PlotThread()
    data_thread.start()
    plot_thread.start()
    data_thread.join()
    plot_thread.join()
