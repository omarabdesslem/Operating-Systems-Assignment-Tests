#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <math.h>
# include <arpa/inet.h>
#include "common.h"

#define SLEEP_TIME 1  //time to sleep between two read of the client

// The client take two inputs: the ip (ipv4 format)
// and the port of the server
int main(int argc, char *argv[]) {
    
    //Check number of input args
    if(argc != 3) {
        fprintf(stderr, "Usage:\n\t%s ip port\n", argv[0]);
        return 1;
    }

    // Convert port input to port number
    uint16_t port = string_to_port(argv[2]);

    // Convert ip input to address stucture
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    if( inet_pton(AF_INET, argv[1], &server_addr.sin_addr) != 1 ) {
        fprintf(stderr, "%s is not a valid ip or ip sockets not supported by your system\n", argv[1]);
        exit(EXIT_FAILURE);
    }

    // Create socket which will be used to communicate with the server
    int socket_server = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_server == -1)
        die("socket");

    // Connect to server
    if( connect(socket_server, (struct sockaddr*) &server_addr, sizeof(server_addr)) == -1 )
        die(argv[1]);

    // First receive the min / max information
    initmsg_t initmsg;
    read_full(socket_server, &initmsg, sizeof(initmsg));

    value_t value; // Our search for a solution
    msg_t msg; // The server answer;
    do {
        // Define a proposition
        value = round(( (float) initmsg.max + initmsg.min) / 2);

        // Propose to server
        printf("Sending proposition: %d\n", value);
        msg.value = value;        
        write_full(socket_server, &msg, sizeof(msg));

        // Get server answer and react
        sleep(SLEEP_TIME);
        read_full(socket_server, &msg, sizeof(msg));
        printf("The true value is: %d, but I am not supposed to know about it.\n", msg.value);
        switch(msg.cmd) {
            case TOO_LOW:
                initmsg.min = value;
                break;
            case TOO_HIGH:
                initmsg.max = value;
                break;
            case WIN:
                printf("I won !!!\n");
                break;
            case LOSE:
                printf("I miserably lost...\n");
                break;
        }
    } while(! (msg.cmd == WIN || msg.cmd == LOSE) );

    close(socket_server);

    return 0;
}