import serial
from matplotlib import pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import telnetlib
import threading
import time

ref_nodes = {}
pos = np.array([[3],[0],[0]])

def grab_and_cal(info):
    global ref_nodes
    global pos
    global ax

    dist = {}
    rough_split = info.split('[')
    if len(rough_split) <= 2:
        return -1
    dis_list = rough_split[1].split(']')[0].split(',')
    if len(dis_list) < 4:
        return -1
    id_list = rough_split[2].split(']')[0].split(',')
    if len(id_list) < 4:
        return -1
    if (len(dis_list) != len(id_list)) | (len(dis_list) < 4):
        return -1
    
    base = ""
    for i in range(0, len(dis_list)):
        id_list[i] = id_list[i].strip('"')
        if id_list[i] in ref_nodes:
            dist[id_list[i]] = (float)(dis_list[i].strip('"'))
            if base == "":
                base = id_list[i]
    
    if len(dist) < 4:
        return -1

    print(dist)
    A = np.array([0,0,0])
    B = np.array([0])
    
    for i in dist:
        if i == base:
            continue
        A = np.vstack((A, ref_nodes[i] - ref_nodes[base]))
        B = np.vstack((B, dist[i]**2 - dist[base]**2 - np.dot(ref_nodes[i]**2 - ref_nodes[base]**2, np.array([1,1,1]))))
    
    A = A[1:len(dist)]
    B = B[1:len(dist)] * (-0.5)
    
    AT = np.transpose(A)
    B = np.dot(AT, B)
    rev = np.linalg.inv(np.dot(AT, A))
    pos = np.dot(rev, B)
    posT = np.transpose(pos)
    # print(posT)

    return 1


def init():
    global ref_nodes
    
    ref_nodes["1818"] = np.array([0, 0, 0])
    ref_nodes["5632"] = np.array([3.2, 0, 0])
    ref_nodes["3884"] = np.array([0, 4.8, 0])
    ref_nodes["1665"] = np.array([2.6, 4.8, 2.15])

class DataThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            raw_data = tn.read_until('\n'.encode())
            data = raw_data.decode(errors='ignore')
            grab_and_cal(data)
        tn.close()

class PlotThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            plt.cla()
            
            ax.scatter(ref_xs, ref_ys, ref_zs, c='b', marker='*')
            ax.scatter([pos[0]], [pos[1]], [pos[2]], c='r', marker='*')
            
            ax.set_xlim3d(-1, 4)
            ax.set_ylim3d(-1, 6)
            ax.set_zlim3d(-0.5, 3)
            plt.pause(0.05)

        plt.show()
    

# -------------------------------------------------------------------------------------------------------------

init()
tn = telnetlib.Telnet(host="127.0.0.1", port=19021)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ref_xs = np.array([ref_nodes["1818"][0], ref_nodes["5632"][0], ref_nodes["3884"][0], ref_nodes["1665"][0]])
ref_ys = np.array([ref_nodes["1818"][1], ref_nodes["5632"][1], ref_nodes["3884"][1], ref_nodes["1665"][1]])
ref_zs = np.array([ref_nodes["1818"][2], ref_nodes["5632"][2], ref_nodes["3884"][2], ref_nodes["1665"][2]])


data_thread = DataThread()
plot_thread = PlotThread()

data_thread.start()
plot_thread.start()

data_thread.join()
plot_thread.join()
