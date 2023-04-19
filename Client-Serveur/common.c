#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdint.h>
#include "common.h"

#define TOO_LOW -1
#define TOO_HIGH 1
#define WIN 0
#define LOOSE 2
#define RAND_PATH "/dev/urandom"
#define RAND_MODE "r"
#define F_MASK 255
#define NB_TRY 4

void die(char* motive){
    printf("%s\n", motive);
    exit(EXIT_FAILURE);
}
//Generating random number from /dev/urandom as a file
uint8_t get_rdm_nbr(){
    FILE* f;
    if( (f = fopen(RAND_PATH, RAND_MODE))  == NULL){
         printf("RANDOM NUMBER GENERATING FAILED\n");
    }
    return fgetc(f);
}
//general function used by clients and server to read in socket
int CSread(int fd, uint16_t *buf){
    int nRead=read(fd,buf,sizeof(*buf));
    if((nRead != 2)){
        printf("SOCKET READING FAILLURE\n");
    }
    return nRead;   
}
//general function used by clients sand server to write
int CSwrite(int fd, uint16_t *buf){
    int nWrite=write(fd,buf, sizeof(*buf));
    if(nWrite != 2){
        printf("SOCKET WRITTING FAILLURE\n");
    }
    return nWrite;       
}
//client side protocol
void client_request(int cfd){   
    fflush(stdout);
    int nb;
    int n=0;
    uint16_t in;
    //loop until winning or n>number of try
    while(n<NB_TRY){
        nb=CSread(cfd, &in);
        //handling different cases for input
        switch (in>>8){
        case TOO_HIGH:
            printf("High %d:%d\n",in>>8, in & F_MASK);
            break;
        case (uint8_t)TOO_LOW:
            printf("Loww %d:%d\n",in>>8, in & F_MASK);
            break;
        case WIN:
            printf("Winn %d:%d\n",in>>8, in & F_MASK);
            exit(EXIT_SUCCESS);
            break;
        case LOOSE:
            printf("Lose %d:%d\n",in>>8, in & F_MASK);
            //exit(EXIT_SUCCESS);
            break;                            
        default:
            printf("Dflt %d:%d\n",in>>8, in & F_MASK);
            break;
        }
        nb=scanf("%hd",&in);
        //exiting if input is not a 2 bytes sized integer
        if(nb==0){
            printf("SCANFING FAILLURE\n");
            break;
        }
        in=in<<8;
        n++;
        nb=CSwrite(cfd,&in);
        
    }
    printf("End of Session %d == NB_TRY\n",n);
}
//server side protocol
void handleClient( int cfd, pid_t pid) {
    int n=1;
    int nbr,nbw;
    uint8_t rdm,strt,end;
    uint16_t buf;
    rdm=get_rdm_nbr();
    strt=(rdm)+-10;
    end=(rdm)+10;
    buf=((strt<<8) | end);//first byte (left is start) right is end
    //sending range to client
    CSwrite(cfd,&buf);
    printf("[%d]Random number choosed : %d\n",pid,rdm);

    while (n<=NB_TRY){
        nbr=CSread(cfd,&buf);
        if(nbr<=0)
            break;
        //handling different cases
        if((buf>>8) == rdm){
            printf("[%d]Win %d %d:%d\n",pid,n,buf>>8, buf & F_MASK);
            buf=(WIN<<8) | WIN;
            CSwrite(cfd,&buf);
            break;
        }else{
            if((buf>>8)<rdm){
                printf("[%d]Low %d %d:%d\n",pid,n,buf>>8, buf & F_MASK);
                buf=(TOO_LOW<<8) | rdm;
                CSwrite(cfd,&buf);
            }else{
                printf("[%d]High %d %d:%d\n",pid,n,buf>>8, buf & F_MASK);
                buf=(TOO_HIGH<<8) | rdm;
                CSwrite(cfd,&buf);           
            }
            n++;
            continue;
        }
    }
    buf=(LOOSE>>8) | LOOSE;
    if(n==4)
        CSwrite(cfd,&buf);   
    close( cfd );
    }

static int main(int argc, char* argv[]){
    get_rdm_nbr();
}