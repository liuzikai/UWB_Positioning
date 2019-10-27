#ifndef SERVER_H
#define SERVER_H

#include "distributed_node.h"
#include "packet.h"
#include "stdio.h"
#include "string.h"

#define STATIC_NODE_NUM     4
#define SERVER_FAIL

int32_t init_static_nodes();

int32_t cal_dis(distributed_node_t* myNode, distributed_node_t* nodes, packet_t* packet_list);

#endif
