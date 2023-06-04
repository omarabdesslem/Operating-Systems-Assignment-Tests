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

int make_client_socket(char* adr_str, uint16_t adr_prt){
    printf("**************** CLIENT ****************\n");
    int result,sock;
    //CREATE SOCKET
    sock=socket(AF_INET, SOCK_STREAM,0);
    if(sock == -1)
        die("Socket création faillure\n");
    //CREATE ADRESS
    struct sockaddr_in saddr;
    memset(&saddr, 0, sizeof(saddr));
    saddr.sin_family=AF_INET;
    saddr.sin_port=htons(adr_prt);
    result=inet_pton(AF_INET,adr_str,&saddr.sin_addr);
    if (result<1)
        die("Adresse ou famille non valide \n");
    //CONNECT SOCKET TO SERVER ADRESS
    result=connect(sock, (struct sockaddr *)&saddr, sizeof(saddr));
    if(result ==-1)
        die("Socket CONNECTING faillure");
    printf("Socket connected to server ip %s, port %d\n",adr_str, adr_prt);
    return sock;
}
int main(int argc,char* argv[]){
    int port,cfd;
    char * adress;
    if(argc !=3)
        die("Invalid synthax");

    adress=argv[1];
    port=atoi(argv[2]);

    cfd=make_client_socket(adress,port);
    client_request(cfd);

}