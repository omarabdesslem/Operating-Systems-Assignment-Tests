//
// Created by antoine on 09.11.22.
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include "functions.h"

int initConnexion(int socket);
int handleClient(int socket, int number, int numTries);

int main(int argc, char *argv[]){
    if(argc < 2){
        fprintf(stderr, "Error no port number given\n");
        return -1;
    }
    FILE *fp = fopen("/dev/urandom", "r"); //ouvrir le fichier pour les nombres aléatoires
    int p = atoi(argv[1]);
    if((p < 1024) || (p > 65535)){
        fprintf(stderr, "Error port number must be between 1024 and 65535\n");
        return -1;
    }
    uint16_t port_num = atoi(argv[1]);

    struct sockaddr_in address;
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(INADDR_ANY);
    address.sin_port = htons( port_num);

    int serverSock = socket(AF_INET, SOCK_STREAM, 0);
    bind( serverSock, (struct sockaddr *) &address, sizeof(address) );
    listen(serverSock, 10); //taille de file d'attente arbitraire pour si plusieurs connexions arrivent en même temps
    printf("En attente de connections\n");

    while( 1 ) {
        struct sockaddr_in clientAddress;
        unsigned int clientLength = sizeof(clientAddress);
        int clientSock = accept(serverSock,
                                (struct sockaddr *) &clientAddress,
                                &clientLength);
        printf( "Client %d connecté avec l'ip %s\n", clientSock, inet_ntoa(clientAddress.sin_addr));
        initConnexion(clientSock);

        pid_t t_pid = fork();
        if(t_pid == 0) {
            int number;
            int numTries = 0;
            do {
                fread(&number, sizeof(int), 1, fp);
            } while((number < 0) || (number > 255));
            printf("La valeur %d est choisie pour le client %d\n", number, clientSock);
            pid_t pid = fork();
            if(pid == 0) {
                while (handleClient(clientSock, number, ++numTries) == 0);
                if(close(clientSock) < 0){
                    fprintf(stderr, "Error closing socket %d: %s", clientSock, strerror(errno));
                }
                exit(EXIT_SUCCESS);
            }
            else if(pid > 0){
                exit(EXIT_SUCCESS);
            }
            else{
                fprintf(stderr, "Could not fork\n");
                return -1;
            }
        }
        else if(t_pid > 0) {
            int wstatus;
            pid_t end = waitpid(t_pid, &wstatus, 0);
            if (end < 0) { printf("Problem %s\n", strerror(errno)); };
        }
        else{
            fprintf(stderr, "Could not fork\n");
            return -1;
        }
    }
}

int handleClient(int socket, int number, int numTries){
    int buffer[2];
    if(receiveMessage(socket, buffer) < 0){return -1;};
    printf("Client %d propose %d\n",socket ,buffer[1]);
    int proposition = buffer[1];
    if(proposition == number){
        int message[2] = {WIN, number};
        if(sendMessage(socket, message) < 0){return -1;};
        printf("Client %d gagne\n", socket);
        return 1;
    }
    if(numTries >= MAX_NUM_TRIES){
        int message[2] = {LOSE, number};

        if(sendMessage(socket, message) < 0){return -1;}
        printf("Client %d perds\n", socket);
        return 1;
    }
    if(proposition < number){
        int message[2] = {TOO_LOW, number};

        if (sendMessage(socket, message) < 0) { return -1; };
    }
    if(proposition > number){
        int message[2] = {TOO_HIGH, number};
        if(sendMessage(socket, message) < 0){return -1;};
    }
    return 0;
}

int initConnexion(int socket){
    int init[2] = {0, 255};
    if(sendMessage(socket, init) < 0){return -1;};
    return 0;
}
