#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>

#define die(msg) do { perror(msg); exit(errno); } while(0);

typedef uint8_t value_t; //The type of the value to send

// The type of the init message sent by the server
// specifies min and max values
typedef struct {
    value_t min;
    value_t max;
} initmsg_t;



// The type of the message exchanged between client and server
typedef struct {
    int8_t cmd;
    value_t value;
} msg_t;

// the cmd member can take the following values
#define TOO_LOW -1
#define WIN 0
#define TOO_HIGH 1
#define LOSE 2

// This fonction takes a string as input and convert it to a 
// uint16_t. It stops the program with an error message if the
// string does not correspond to an integer fitting an uint16_t
uint16_t string_to_port(const char*);

// This function attempts to read on the file descriptor 
// count bytes of data. It outputs an error and exit if: 
// - a read call returns 0 (no more data on fd)
// - a read call returns an error
void read_full(int, void*, size_t);

// This function attempts to write on the file descriptor 
// count bytes of data. It outputs an error and exit if: 
// - a write call returns 0 (no more space on fd)
// - a write call returns an error
void  write_full(int, const void*, size_t);
