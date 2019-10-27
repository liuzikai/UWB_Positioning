#include "server.h"

static packet_t packets[MAX_PACKET_NUM];
static distributed_node_t static_nodes[STATIC_NODE_NUM];
static distributed_node_t myNode;

int32_t init_static_nodes(){
    /* Clear the static_nodes array */
    memset(static_nodes, 0, sizeof(distributed_node_t) * STATIC_NODE_NUM);

    /** Fill the static_nodes array **/

    /* Node 0 */
    static_nodes[0].id = 0;
    static_nodes[0].x = 1000;
    static_nodes[0].y = 1000;
    static_nodes[0].z = 1000;

    /* Node 1 */
    static_nodes[1].id = 1;
    static_nodes[1].x = 1000;
    static_nodes[1].y = 1000;
    static_nodes[1].z = 1000;
    
    /* Node 2 */
    static_nodes[2].id = 2;
    static_nodes[2].x = 1000;
    static_nodes[2].y = 1000;
    static_nodes[2].z = 1000;

    /* Node 3 */
    static_nodes[3].id = 3;
    static_nodes[3].x = 1000;
    static_nodes[3].y = 1000;
    static_nodes[3].z = 1000;
}

int32_t cal_dis(distributed_node_t* myNode, distributed_node_t* nodes, packet_t* packet_list){
    
}
