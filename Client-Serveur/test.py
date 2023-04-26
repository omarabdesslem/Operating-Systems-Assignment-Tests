#!/usr/bin/env python3
import argparse
import socket
import struct
import sys
import random  # for ip adress generation

##valeurs par defaults
number_servers = 5
NB_TRY = 10
TOO_HIGH = 1
TOO_LOW = -1
WIN = 0
LOOSE = -2
F_MASK = 0xFF
IP = "127.0.0.1"


class bcolors:
    ENDC = '\033[0m'
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Grey = '\033[90m'
    Black = '\033[90m'

    def disable(self):
        self.Red = ''
        self.Green = ''
        self.Blue = ''
        self.Cyan = ''
        self.White = ''
        self.Yellow = ''
        self.Magenta = ''
        self.Grey = ''
        self.Black = ''
        self.ENDC = ''


test_failed = False


def test(func, *args):
    def wrapper(self, *args):
        global test_failed
        print(func.__name__.upper() + ": ", end="")
        try:
            func(self, *args)
        except (AssertionError, FileNotFoundError, Exception, OSError, AttributeError) as e:
            print(bcolors.Red + "FAILED" + bcolors.ENDC)
            print(str(e))
            test_failed = True
        else:
            print(bcolors.Green + "SUCCESS" + bcolors.ENDC)

    return wrapper


class Test():
    def generate_random_ip(self):
        octets = [random.randint(0, 255) for i in range(4)]  # generation de 4 octets random
        ip_address = '.'.join(str(octet) for octet in octets)
        print(ip_address)
        return ip_address

    def check_ip_in_use(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            print("IP IN USE")
            return True
        else:
            print("IP NOT IN USE")
            return False


    def connect_to_server(self, host, port):
        # create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect_ex((host, port))
        print('Connected to server')
        return client_socket

    @test
    def test_connect(self, client_socket):
        if client_socket is None:
            raise Exception(f"Client server connection failed")


    def client_request(self, cfd):
        sys.stdout.flush()
        end, start = struct.unpack('BB', cfd.recv(2))
        #'BB': two byte sized ints
        #retourne deux objects d'unpacked format, ici c'est u_int8t

        #status = cfd.recv(1).decode('utf-8')  # donnèes entrantes du serveur #doesn't work
        #data = ctypes.c_int8(int(cfd.recv(1)))
        # u_int8t n'existe pas en Py, on utilise ctypes
        #status = ctypes.c_int8(int(status))
        print(end, start)

        guess = random.randint(0, 255)  #on envoit un guess random au début, pour recevoir la réponse correcte

        buf = (guess << 8) | 0  # GUESS | 0 0 0 0 0 0 0 0 0 pour que le second byte soit set to 0
        client_socket.sendall(struct.pack('>H', buf))
        #>H: signed short integer, 2 octets, big endian >

        data = client_socket.recv(2)
        number, response = struct.unpack('>BB', data)
        print(response, number)

        buf = number | 0  # GUESS | 0 0 0 0 0 0 0 0 0 pour que le second byte soit set to 0
        client_socket.sendall(struct.pack('>H', buf))

        data = client_socket.recv(2)
        number, response = struct.unpack('>BB', data)
        print(response, number)
        #ça sera une fonction handle, pour tester low, high, etc..
        switch = {
            TOO_HIGH: 'High',
            TOO_LOW: 'Low',
            WIN: 'Win',
            LOOSE: 'Lose'
        }
        if response == WIN:
            print(f'WIN! You guessed the number {number}')

        elif response == TOO_LOW % 256: #le mod est tres important, too low donne 255
            print(f'The number is higher than {guess}')
            start = number
        elif response == TOO_HIGH:
            print(f'The number is lower than {guess}')
            end = number

    def multiple_clients_test(self, port, n):
        for i in range(n):

            #getting a valid ip
            host = self.generate_random_ip()
            #while (self.check_ip_in_use(host, port)):
            #    host = self.generate_random_ip()
            #connect to server function
            client_socket = self.connect_to_server(host, port)
            #test connection
            self.test_connect(client_socket)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test pour verifier le bon fonctionnement de votre TP')
    parser.add_argument('program_name', type=str, help='path de votre programme digest')
    parser.add_argument('port', type=int, help='port number for server connection')
    parser.add_argument('-i', '--ip_adress', type=str, help='prend une adresse ip comme agrument')
    args = parser.parse_args()
    program_name = args.program_name
    PORT = args.port
    if args.ip_adress:
        IP = args.ip_adress
    t = Test()
    print(bcolors.Magenta + '--- BEGIN TEST ---\n' + bcolors.ENDC)
    client_socket = t.connect_to_server(IP, PORT)
    t.test_connect(client_socket)
    #t.multiple_clients_test(PORT, number_servers)
    t.client_request(client_socket)
    print(bcolors.Magenta + '--- END TEST ---' + bcolors.ENDC)
