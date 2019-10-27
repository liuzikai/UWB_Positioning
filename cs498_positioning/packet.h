#ifndef PACKET_H
#define PACKET_H

#include "stdint.h"
#include "string.h"
#include "stdbool.h"
#include "stdlib.h"

#define MAX_PACKET_NUM      6
#define MIN_PACKET_NUM      4
#define DATA_LENGTH         10
#define PACKET_FAIL         -1

typedef struct packet_t{
    int32_t id;
    int32_t dis;
}packet_t;

int32_t fill_packet(packet_t* packet_list, char* packet_info);

#endif
