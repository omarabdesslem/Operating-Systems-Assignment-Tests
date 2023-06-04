//
// Created by antoine on 14.11.22.
//
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "functions.h"

#define BUFF_SIZE 2*sizeof(int)

int sendMessage(int socket, int buffer[]){
    size_t n_sent = write(socket, buffer, BUFF_SIZE);
    if( n_sent < BUFF_SIZE){
        fprintf(stderr, "Error sending message\n");
        return -1;
    }
    return 0;
}


int receiveMessage(int socket, int buffer[]){
    size_t n_read = read(socket, buffer, BUFF_SIZE);
    if(n_read <= 0){
        fprintf(stderr, "Error reading message\n");
        return -1;
    }
    return 0;
}
