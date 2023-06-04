#include "common.h"

// This fonction takes a string as input and convert it to a 
// uint16_t. It stops the program with an error message if the
// string does not correspond to an integer fitting an uint16_t
uint16_t string_to_port(const char *str) {
    // Convert input in port number
    errno = 0;
    long int port = strtol(str, NULL, 10);
    if (errno != 0)
        die("port value");

    // Check long int fit in uint16 (as it is the returned value)
    if (port > UINT16_MAX) {
        errno = ERANGE;
        die("port value");
    }

    // If port == 0 either no valid numerical value was found or 0 was found
    // none is a valid port
    if (port == 0) {
        fprintf(stderr, "%s is not a valid port\n", str);
        exit(1);
    }

    return port;
}

// This function attempts to read on the file descriptor 
// count bytes of data. It outputs an error and exit if: 
// - a read call returns 0 (no more data on fd)
// - a read call returns an error
void read_full(int fd, void* buff, size_t count) {
    ssize_t nb_read;
    do {
        nb_read = read(fd, buff, count);
        if ( nb_read == -1)
            die("read_full");
        if (nb_read == 0) {
           fprintf(stderr, "read_full: file descriptor end is reached before count bytes were read\n");
           exit(EXIT_FAILURE);
        }
        count -= nb_read;
        buff +=  nb_read;
    } while(count > 0);
}

// This function attempts to write on the file descriptor 
// count bytes of data. It outputs an error and exit if: 
// - a write call returns 0 (no more space on fd)
// - a write call returns an error
void write_full(int fd, const void* buff, size_t count) {
    ssize_t nb_write;
    do {
        nb_write = write(fd, buff, count);
        if ( nb_write == -1)
            die("write socket");
        if (nb_write == 0) {
           fprintf(stderr, "write_full: file descriptor end is reached before count bytes were written\n");
           exit(EXIT_FAILURE);
        }
        count -= nb_write;
        buff +=  nb_write;
    } while(count > 0);
}
