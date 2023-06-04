//
// Created by antoine on 14.11.22.
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <errno.h>
#include "functions.h"

int initConnexion(int socket);
int handleConnexion(int socket);

int main(int argc, char *argv[]){
    if(argc < 3){
        fprintf(stderr, "Error not enough arguments\n");
        return -1;
    }
    char *host = argv[1];
    uint16_t port_num = atoi(argv[2]);

    struct sockaddr_in address;
    memset( &address, 0, sizeof(address) );
    inet_pton( AF_INET, host, &(address.sin_addr) );
    address.sin_family = AF_INET;
    address.sin_port = htons(port_num);

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if(connect(sock, (struct sockaddr *) &address, sizeof(address)) < 0){
        fprintf(stderr, "Error connecting to server %s\n", strerror(errno));
        return -1;
    }

    initConnexion(sock);
    while(handleConnexion((sock)) == 0);

    return 0;
}

int handleConnexion(int socket){
    int buffer[2];
    buffer[0] = 0;
    scanf("%d", &buffer[1]);
    if((buffer[1] < 0) || (buffer[1] > 255)){
        fprintf(stderr, "Value must be between 0 and 255\n");
        return 0;
    }
    if(sendMessage(socket, buffer) < 0){return -1;};
    printf("Proposition envoyée %d\n", buffer[1]);
    int answer[2];
    if(receiveMessage(socket, answer) < 0){return -1;};
    printf("La valeur réelle est %d\n", answer[1]);
    int correct = answer[0];
    if(correct == WIN){
        printf("Victoire\n");
        return 1;
    }
    if(correct == LOSE){
        printf("Défaite\n");
        return 1;
    }
    if(correct == TOO_HIGH){
        printf("La valeur proposée est trop élevée\n");
    }
    if(correct == TOO_LOW){
        printf("La valeur proposée est trop basse\n");
    }
    return 0;
}

int initConnexion(int socket){
    printf("En attente du serveur\n");
    int init[2];
    if(receiveMessage(socket, init) < 0){return -1;};
    printf("Le nombre est entre %d et %d\n", init[0], init[1]);
    return 0;
}