#!/usr/bin/env python3

import socket
import os

def handle_connection(client_socket):
    # handle incoming data
    data = client_socket.recv(1024)
    print("Received data: %s" % data.decode())
    
    # send response
    response = "Hello, client!\r\n".encode()
    client_socket.send(response)
    
    # close connection
    client_socket.close()

def serve(port):
    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # bind socket to port
    server_socket.bind(('', port))
    
    # listen for incoming connections
    server_socket.listen(5)
    print("Listening on port %d..." % port)
    
    while True:
        # accept incoming connection
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from %s:%d" % client_address)
        
        # fork process to handle connection
        pid = os.fork()
        
        if pid == 0:
            # child process
            server_socket.close() # close server socket in child process
            handle_connection(client_socket)
            os._exit(0) # exit child process
        else:
            # parent process
            client_socket.close() # close client socket in parent process

if __name__ == "__main__":
    port = int(input("Enter port number: "))
    serve(port)
