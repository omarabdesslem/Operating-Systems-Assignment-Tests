#!/usr/bin/env python3
import argparse
import random
import socket
import struct
import sys
import subprocess
import string  # for client names
import time  # for waiting
import multiprocessing #for launching multiple clients simultaneously

##valeurs par defaults
number_servers = 5
NB_TRY = 10
TOO_HIGH = 1
TOO_LOW = -1
WIN = 0
LOOSE = -2
F_MASK = 0xFF
# IP = "10.194.68.29"
IP = "127.0.0.1"


# lancer serveur de l'etudiant
# choisir port

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

    def wait(self):
        period = random.uniform(2, 5)
        time.sleep(period)

    @test
    def launch_program(self):
        terminal_command = f'gnome-terminal -- bash -c "{program_name} {str(PORT)}; exec bash"'

        # lancer le terminal avec cette commande, shell = True pour prendre la commande en totale, pas comme une liste d'args
        subprocess.run(terminal_command, shell=True)
        self.wait()

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

    def play(self, cfd):

        sys.stdout.flush()
        mode = 0
        for i in range(NB_TRY):
            data = cfd.recv(8)
            try:
                begin, end = struct.unpack('ii', data)
            except (SyntaxError, struct.error) as e:
                try:
                    begin, end = struct.unpack('HH', data)
                    mode = 1
                except (SyntaxError, struct.error) as e:
                    try:
                        print(f"try {i}\n")
                        begin, end = struct.unpack('BB', data)
                        mode = 2
                    except:
                        begin, end = struct.unpack('B', data)
                        mode = 3

            print(f"mode = {mode}\ntaille = {len(data)}\n")
            print(f"received: {begin, end}\nrecv_packed_data: {data}\n")
            switch = {
                TOO_HIGH: 'High',
                TOO_LOW: 'Low',
                WIN: 'Win',
                LOOSE: 'Lose'
            }
            print(f"High/Low value ={begin}")
            if begin == WIN:
                if i > 0:
                    print(f'WIN! You guessed the number {end}')
                    cfd.close()
                    break
            elif begin == TOO_LOW % 256 or begin == TOO_LOW:  # le mod est tres important, too low donne 255
                print(f'The number is too low: {end}')
            elif begin == TOO_HIGH:
                print(f'The number is too high than {end}')
            elif begin == LOOSE:
                print(f'YOU LOOSE, number= {end}')
                cfd.close()
                break
            guess = int(input(f"Ecrire ton guess entre: {begin} {end}\n"))
            if mode == 0:
                packed = struct.pack('ii', 0, guess)
            if mode == 1:
                packed = struct.pack('i', guess)
            if mode == 2:
                packed = struct.pack('>H', guess)
                print(f"sent: {begin}, sent_packed_data: {packed} ")
            if mode == 3:
                packed = struct.pack('ii', 0, guess)

            print(f"sent: {guess}, sent_packed_data: {packed} ")
            cfd.sendall(packed)
        cfd.close()

    @test
    def client_request(self, cfd):
        sys.stdout.flush()
        mode = 0
        for i in range(NB_TRY):
            data = cfd.recv(8)
            try:
                begin, end = struct.unpack('ii', data)
            except (SyntaxError, struct.error) as e:
                try:
                    begin, end = struct.unpack('HH', data)
                    mode = 1
                except (SyntaxError, struct.error) as e:
                    try:
                        begin, end = struct.unpack('BB', data)
                        mode = 2
                    except:
                        begin, end = struct.unpack('B', data)
                        mode = 3
            switch = {
                TOO_HIGH: 'High',
                TOO_LOW: 'Low',
                WIN: 'Win',
                LOOSE: 'Lose'
            }
            if begin == WIN:
                if i > 0:
                    print(f'WIN! You guessed the number {end}')
                    break
            elif begin == TOO_LOW % 256:  # le mod est tres important, too low donne 255
                print(f'The number is higher than {end}')
            elif begin == TOO_HIGH:
                print(f'The number is lower than {end}')

            print(f"mode = {mode}\ntaille = {len(data)}\n")
            print(f"received: {begin, end}\nrecv_packed_data: {data}\n")
            print(f"\n---- TRY ---- {i}\n")

            if mode == 0:
                packed = struct.pack('ii', 0, end)
            if mode == 1:
                packed = struct.pack('i', end)
            if mode == 2:
                packed = struct.pack('>H', begin)
                print(f"sent: {begin}, sent_packed_data: {packed} ")
            if mode == 3:
                packed = struct.pack('ii', 0, end)

            print(f"sent: {begin}, sent_packed_data: {packed} ")
            cfd.sendall(packed)
        cfd.close()


    def handle_client(self):
        client_socket = t.connect_to_server(IP, PORT)
        self.client_request(client_socket)
    @test
    def multiple_clients_test_interactive(self, n):
        # liste des processus
        processes = []
        for i in range(n):
            p = multiprocessing.Process(target=self.handle_client)
            p.start()
            processes.append(p)

        # Wait for all client processes to finish
        for p in processes:
            p.join(5)  # blocks until the process whose join() method is called terminates
        self.wait()
        for p in processes:
            p.terminate()  # ne marche pas

    @test
    def client_process(self):
        # connect to server function
        client_socket = self.connect_to_server(IP, PORT)
        while True:
            data = client_socket.recv(8)
            client_socket.sendall(bytearray(2))
            # test connection
            self.test_connect(client_socket)

    @test
    def multiple_clients_test_dummy(self, n):
        # liste des processus
        processes = []
        for i in range(n):
            p = multiprocessing.Process(target=self.client_process)
            p.start()
            processes.append(p)

        # Wait for all client processes to finish
        for p in processes:
            p.join(5) #blocks until the process whose join() method is called terminates

        for p in processes:
            p.terminate() #ne marche pas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test pour verifier le bon fonctionnement de votre TP')
    parser.add_argument('program_name', type=str, help='path de votre programme digest')
    parser.add_argument('port', type=int, help='port number for server connection')
    parser.add_argument('-i', '--ip_adress', type=str, help='prend une adresse ip comme agrument')
    parser.add_argument('-p', action='store_true', help='test toi même  les valeurs à envoyer au Serveur')
    args = parser.parse_args()
    program_name = args.program_name
    PORT = args.port
    if args.ip_adress:
        IP = args.ip_adress
    t = Test()
    print(bcolors.Magenta + '--- BEGIN TEST ---\n' + bcolors.ENDC)
    t.launch_program()
    client_socket = t.connect_to_server(IP, PORT)
    t.test_connect(client_socket)
    if args.p:
        t.play(client_socket)
    else:
        t.client_request(client_socket)
        t.multiple_clients_test_interactive(number_servers)
        t.multiple_clients_test_dummy(number_servers)
    print(bcolors.Magenta + '--- END TEST ---' + bcolors.ENDC)
