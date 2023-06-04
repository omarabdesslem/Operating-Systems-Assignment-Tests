#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "common.h"

#define QUEUE_SIZE 4
int make_server_socket(uint16_t port){
    int result,sock;
    //CREATE SOCKET
    sock=socket(AF_INET, SOCK_STREAM,0);
    if(sock == -1)
        die("Socket création faillure\n");
    //CREATE ADRESS
    struct sockaddr_in saddr;
    memset(&saddr, 0, sizeof(saddr));
    saddr.sin_family=AF_INET;
    saddr.sin_port=htons(port);
    saddr.sin_addr.s_addr=htonl(INADDR_ANY);

    //BIND SOCKET TO ANY ADRESS
    result=bind(sock, (struct sockaddr *)&saddr, sizeof(saddr));
    if(result ==-1)
        die("Socket binding faillure");
    //LSTENING CONNECTIONS
    result=listen(sock, QUEUE_SIZE);
    if(result ==1)
        die("Socket listening faillure");
    
    return sock;
}
//server protocol
void server_accept(int sfd){
    printf("**************** SERVER ****************\n");
    while(1){//loop in which we are accepting clients
        char * adr_str=malloc(16);
        struct sockaddr_in caddr;
        socklen_t caddr_len=sizeof(caddr);
        int cfd=accept(sfd, (struct sockaddr *)&caddr, &caddr_len);
        if(cfd < 0)
            die("Accepting client faillure\n");
        printf("++++++++++++++++++++++++++++++++++++++\nAccepting client  ip: %s socket : %d\n",inet_ntoa(caddr.sin_addr),caddr.sin_port);
        pid_t pid = fork();//Making child process
        if(pid > 0){
            continue;//parent continue looping
        }else if(pid==0){
            pid_t pid=getpid();
            handleClient(cfd,pid);//child process handleclient
        }else{
            printf("FORKING TO CHILD PROCESS FAILLURE\n");
        }      
    }
}

int main(int argc, char* argv[]){
    int port;
    //checking if valid synthaxe
    if(argc != 2)
        die("Invalid Synthax %d");
    //running server
    port=atoi(argv[1]);    
    int serv_fd=make_server_socket(port);
    server_accept(serv_fd);

}
