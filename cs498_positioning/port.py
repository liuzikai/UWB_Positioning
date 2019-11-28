import serial
import numpy as np
import telnetlib

ref_nodes = {}
pos = np.array([0])

def grab_and_cal(info):
    global ref_nodes
    global pos
    # print(info)
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
    # print(A)
    rev = np.linalg.inv(np.dot(AT, A))
    pos = np.dot(rev, B)
    posT = np.transpose(pos)
    print(posT)
    return 1


def init():
    global ref_nodes
    
    ref_nodes["1818"] = np.array([0, 0, 0])
    ref_nodes["5632"] = np.array([3.2, 0, 0])
    ref_nodes["3884"] = np.array([0, 4.8, 0])
    ref_nodes["1665"] = np.array([2.6, 4.8, 2.15])

def command(con, flag):
    data = con.read_until(flag.encode())
    print(data.decode(errors='ignore'))
    return data



init()
# print(ref_nodes)
# print(grab_and_cal("{{rng:[\"3256\",\"2222\",\"3808\",\"1189\"], \"uid\": [\"1818\",\"5632\",\"3884\",\"1665\"]}}"))
# serial_name = ''
# ser = serial.Serial(serial_name)
# while True:
#     line = ser.readline()
#     grab_and_cal(line)
tn = telnetlib.Telnet(host="127.0.0.1", port=19021)
# grab_and_cal("{\"utime\": 1322787487,\"nrng\": {\"seq\": 193,\"mask\": 15,\"rng\": [\"3.513\",\"3.909\",\"2.267\",\"2.680\"],\"uid\": [\"1818\",\"5632\",\"3884\",\"1665\"]}}")
while True:
    raw_data = tn.read_until('\n'.encode())
    data = raw_data.decode(errors='ignore')
    # print(data)
    grab_and_cal(data)

tn.close()  