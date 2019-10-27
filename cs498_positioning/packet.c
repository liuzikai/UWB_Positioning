#include "packet.h"

int32_t fill_packet(packet_t* packet_list, char* packet_info){
    /* Get the length of the packet_info */
    size_t str_len = strlen(packet_info);
    /* Find the start of the data part */
    char* dis_start = memchr(packet_info, '[', str_len);
    /* Find the end of the data part */
    char* dis_end = memchr(packet_info, ']', str_len);
    /* Get the lenght of the rest of the packet_info */
    size_t rest_len = strlen(dis_end + 1);
    /* Find the start of the id part */
    char* id_start = memchr(dis_end + 1, '[', rest_len);
    /* Find the end of the id part */
    char* id_end = memchr(dis_end + 1, ']', rest_len);
    /* Get the length of the data part */
    uint32_t dis_len = (uint32_t)(dis_end) - (uint32_t)(dis_start);
    /* Get the length of the id part */
    uint32_t id_len = (uint32_t)(id_end) - (uint32_t)(id_start);
    /* Create the data array */
    char data_array[dis_len + 1];
    /* Create the id array */
    char id_array[id_len + 1];
    /* Fill the data array */
    memmove(data_array, dis_start, dis_len);
    data_array[dis_len] = '\0';
    /* Fill the id array */
    memmove(id_array, id_start, id_len);
    id_array[id_len] = '\0';
    
    /* Grab the data */
    int32_t dis_read_count = 0;
    char data[DATA_LENGTH]; // container of a piece of data
    char* inspector = dis_start; // iterator to the string
    while(dis_read_count < MAX_PACKET_NUM){
        int8_t per_data_length = 0; // count the length of the data
        bool is_data = false; // indicating whether present character belongs to data
        while (inspector != dis_end){
            if(&inspector == '"'){
                is_data = !is_data; // the first '"' will set it true, the second '"' will set it false
                if(!is_data){
                    data[per_data_length++] = '\0';
                    break;
                }
            }else if(is_data){
                data[per_data_length++] = &inspector;
            }
            inspector++;
        }
        if(inspector == dis_end){
            break;
        }else{
            packet_list[dis_read_count++].dis = atoi(data);
        }
    }

    /* Grab the id */
    int32_t id_read_count = 0;
    inspector = id_start; // iterator to the string
    while(id_read_count < MAX_PACKET_NUM){
        int8_t per_data_length = 0; // count the length of the data
        bool is_data = false; // indicating whether present character belongs to data
        while (inspector != id_end){
            if(&inspector == '"'){
                is_data = !is_data; // the first '"' will set it true, the second '"' will set it false
                if(!is_data){
                    data[per_data_length++] = '\0';
                    break;
                }
            }else if(is_data){
                data[per_data_length++] = &inspector;
            }
            inspector++;
        }
        if(inspector == id_end){
            break;
        }else{
            packet_list[id_read_count++].id = atoi(data);
        }
    }

    if(dis_read_count == id_read_count){
        return dis_read_count;
    }else{
        return PACKET_FAIL;
    }
}
