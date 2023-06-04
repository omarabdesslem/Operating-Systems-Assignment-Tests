//
// Created by antoine on 14.11.22.
//

#ifndef SYSTEMES_EXPLOITATION_FUNCTIONS_H
#define SYSTEMES_EXPLOITATION_FUNCTIONS_H

#define TOO_LOW -1
#define TOO_HIGH 1
#define WIN 0
#define LOSE 2
#define MAX_NUM_TRIES 5

int sendMessage(int socket, int buffer[]);
int receiveMessage(int socket, int buffer[]);

#endif //SYSTEMES_EXPLOITATION_FUNCTIONS_H
