#!/usr/bin/env python3

import argparse
import socket
import sys
import random  # for ip adress generation

##valeurs par defaults
number_servers = 5
NB_TRY = 10
TOO_HIGH = 1
TOO_LOW = 2
WIN = 3
LOOSE = 4
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
        return ip_address

    def connect_to_server(self, host, port):
        # create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print('Connected to server')
        return client_socket

    @test
    def test_connect(self, client_socket):
        if client_socket is None:
            raise Exception(f"Client server connection failed")

    @test
    def client_request(self, cfd):
        sys.stdout.flush()
        n = 0
        action = ''
        while n < NB_TRY:
            data = cfd.recv(2)  # donnèes entrantes du serveur

            if not data:  # on sort si on reçoit pas de donnèes
                break

            entry = int(data[0])

            switch = {
                TOO_HIGH: 'High',
                TOO_LOW: 'Low',
                WIN: 'Win',
                LOOSE: 'Lose'
            }

            if action == 'Win':
                sys.exit(0)
            elif action == 'SCANNING FAILURE':
                break

            entry = int(input())
            if entry > F_MASK:
                print('Input should be between 0 and 255')
                break
            # d = uint8_t(data_to_be_sent)
            cfd.send()  #

    @test
    def multiple_clients_test(self, port, n):
        for i in range(n):
            # create socket
            host = self.generate_random_ip()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            print('Connected to server')
            if socket is None:
                raise Exception(f"Client server connection failed")


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
    t.multiple_clients_test(PORT, number_servers)
    # t.client_request(client_socket)
    print(bcolors.Magenta + '--- END TEST ---' + bcolors.ENDC)
