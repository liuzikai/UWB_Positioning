import serial
import numpy as np

ref_nodes = {}
pos = np.array([0])

def grab_and_cal(info):
    global ref_nodes
    global pos
    dist = {}
    rough_split = info.split('[')
    dis_list = rough_split[1].split(']')[0].split(',')
    id_list = rough_split[2].split(']')[0].split(',')
    
    if (len(dis_list) != len(id_list)) | (len(dis_list) < 4):
        return -1
    
    base = ""
    for i in range(0, len(dis_list)):
        id_list[i] = id_list[i].strip('"')
        if id_list[i] in ref_nodes:
            dist[id_list[i]] = (int)(dis_list[i].strip('"'))
            if base == "":
                base = id_list[i]
    
    if len(dist) < 4:
        return -1

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
    print(pos)
    return 1


# def read_port():


def init():
    global ref_nodes
    
    ref_nodes["1818"] = np.array([3000, 0, 0])
    ref_nodes["5632"] = np.array([0, 2500, 0])
    ref_nodes["3884"] = np.array([0, 1500, 0])
    ref_nodes["1665"] = np.array([0, 0, 800])



init()
print(ref_nodes)
print(grab_and_cal("{{rng:[\"3256\",\"2222\",\"3808\",\"1189\"], \"uid\": [\"1818\",\"5632\",\"3884\",\"1665\"]}}"))

    