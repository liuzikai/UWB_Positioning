#ifndef DISTRIBUTED_NODE_H
#define DISTRIBUTED_NODE_H

#include "stdint.h"
#include "stdbool.h"


typedef struct distributed_node_t{
    int32_t id;
    int32_t x; // mm
    int32_t y; // mm
    int32_t z; // mm
} distributed_node_t;



#endif
