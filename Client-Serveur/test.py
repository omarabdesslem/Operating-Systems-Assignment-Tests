#!/usr/bin/env python3
import argparse
import random
import socket
import struct
import sys
import subprocess
import time  # for waiting
import os
import threading
##TOO HIGH AVANT
##valeurs par defaults
number_servers = 3
NB_TRY = 10
TOO_HIGH = 1
TOO_LOW = -1
WIN = 0
LOOSE = 2
F_MASK = 0xFF

IP = "127.0.0.1"
AUTONOMOUS = 1
USER_CHOICE = 0
test_failed = False
DEBUG = 0  # var globale resets à chaque lancement
Multi_CLIENT_ERROR = 0
Warnings = []
Higher_than_Lower_than_test_mode = 2


# binary color class
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
        period = random.uniform(2, 3)
        time.sleep(period)
        return 0
    def kill_terminal(self):
        if sys.platform == 'win32':
            subprocess.Popen('taskkill /IM cmd.exe /F', shell=True)
        elif sys.platform == 'darwin':
            subprocess.Popen(['osascript', '-e', 'quit app "Terminal"'])
        elif sys.platform.startswith('linux'):
            subprocess.Popen(['killall', 'bash'])

    def check_interface_graphique(self):  # tester si le terminal est graphique avec $Display
        display = os.environ.get('DISPLAY')
        return display is not None

    def get_terminal_command_type_server(self, prog_name, port):

        if DEBUG == 1:
            terminal_command = f'{prog_name}  {str(port)} > server.txt 2>&1'
        else:
            terminal_command = f'{prog_name}  {str(port)} > /dev/null 2>&1'
        return terminal_command

    def get_terminal_command_type_client(self, prog_name, ip, port):
        if DEBUG == 1:
            terminal_command = f'{prog_name} {str(ip)} {str(port)} > client.txt 2>&1'
        else:
            terminal_command = f'{prog_name} {str(ip)} {str(port)} > /dev/null 2>&1'
        return terminal_command

    def generate_port(self):
        while True:
            port_created = random.randrange(10000, 65530)
            if self.check_port_in_use(port_created) == False:
                break
        return port_created

    def print_warnings(self):
        for warning in Warnings:
            print(bcolors.Yellow + warning + bcolors.ENDC)

    # $Terminal lancé avec cette commande
    # si session graphique => nouv terminal, sinon tout sur le meme terminal
    # lancer le terminal avec cette commande, shell = True pour prendre la commande en totale, pas comme une liste d'args
    @test
    def try_launch_server_program(self):
        try:
            subprocess.check_output([f"{program_name}", str(self.generate_port())], timeout=3)
        except subprocess.TimeoutExpired:
            pass
        except (AssertionError, FileNotFoundError, Exception, OSError, AttributeError) as e:
            raise Exception(str(e))

    @test
    def try_launch_client_program(self):
        try:
            subprocess.check_output([f"{program_name}", str(IP), str(PORT)], timeout=3)
        except subprocess.TimeoutExpired:
            pass
        except (AssertionError, FileNotFoundError, Exception, OSError, AttributeError) as e:
            raise Exception(str(e))

    def launch_program(self, program_type):
        if program_type == "server":
            self.try_launch_server_program()
            terminal_command = self.get_terminal_command_type_server(program_name, str(PORT))
        else:
            self.try_launch_client_program()
            terminal_command = self.get_terminal_command_type_client(program_name, str(IP), str(PORT))

        if self.check_interface_graphique:
            launched_terminal = subprocess.Popen(terminal_command, shell=True)
        else:
            os.system(terminal_command)
        if DEBUG == 1:
            print(f"Launched program with terminal command:{terminal_command}")
        self.wait()
        return launched_terminal

    def connect_to_server(self, host, port):
        # create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((host, port))
        except(Exception, OSError, AttributeError) as e:
            return None
        return client_socket

    def check_port_in_use(self, port):
        command = f"netstat -an | grep -w {port}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if DEBUG == 1:
            print(result)
        return len(result.stdout.strip()) != 0

    @test
    def test_connect(self, client_socket):
        if client_socket is None:
            raise Exception(f"Client server connection failed")

    def client_receive(self, cfd):
        sys.stdout.flush()
        data = cfd.recv(8)
        if len(data) == 0:
            print("End of client reception")
            return 0, 0 ,0 ,0
        if len(data) == 1:
            return data, data, 3, data
        else:
            try:
                first_half, second_half = struct.unpack('ii', data)
                mode = 0
            except (SyntaxError, struct.error) as e:
                try:
                    first_half, second_half = struct.unpack('HH', data)
                    mode = 1
                except (SyntaxError, struct.error) as e:
                    try:
                        first_half, second_half = struct.unpack('BB', data)
                        mode = 2
                    except:
                        first_half, second_half = struct.unpack('B', data)
                        mode = 3
            return first_half, second_half, mode, data

#function g(f, [bytes])
    def interact(self, pack_unpack_function, array_of_types, data):
        for i in (array_of_types):
            pack_unpack_function(array_of_types[i], data)
            
    def client_send(self, cfd, guess, mode):

        if mode == 0:
            packed = struct.pack('ii', 0, guess)
        if mode == 1:
            packed = struct.pack('i', guess)
        if mode == 2:
            packed = struct.pack('>H', guess)
        if mode == 3:
            packed = struct.pack('ii', 0, guess)
        cfd.sendall(packed)
        return 0

    def client_request(self, cfd, type):
        min, max, mode, data = self.client_receive(cfd)
        correct_order = 0
        if min > max:
            correct_order = 1
            switcher = min
            min = max
            max = switcher

        guess = random.randrange(min, max)
        self.client_send(cfd, guess, mode)
        saved_sent = guess
        for try_number in range(NB_TRY):
            first_half, second_half, mode, data = self.client_receive(cfd)
            if data == 0:
                break
            if DEBUG == 1:
                print(f"received: {first_half, second_half}  sent: {guess}")
            if type != USER_CHOICE:
                guess = second_half
                if try_number > 1:
                    guess = first_half
                if type == 2:
                    correct_number = guess
                    guess = random.randrange(min, max)
                    if DEBUG ==1:
                        print(guess)
            else:
                guess = int(input(f"Ecrire ton guess entre: {first_half} {second_half}\n"))

            switch = {
                TOO_HIGH: 'High',
                TOO_LOW: 'Low',
                WIN: 'Win',
                LOOSE: 'Lose'
            }
            if first_half == WIN:
                if try_number > 0:
                    break
            if first_half == TOO_HIGH:
                if type == 2:
                    if saved_sent <= correct_number:
                        raise Exception(f"TOO HIGH NOT WORKING: sent : {saved_sent} <= {correct_number}, check if inputed the right values -v, and right number of tries ")
            elif first_half == TOO_LOW:
                if type == 2:
                    if saved_sent >= correct_number:
                        raise Exception(f"TOO LOW NOT WORKING: sent : {saved_sent} <= {correct_number}, check if inputed the right values -v, and right number of tries ")
            elif first_half == LOOSE:
                if try_number > 1:
                    if type == 2:
                        if try_number != NB_TRY-1:
                            raise Exception(
                                f"LOST before correct number of tries: program try number : {try_number}!= {NB_TRY} number of maximum assigned tries ")
                    break
            saved_sent = guess
            self.client_send(cfd, guess, mode)
        cfd.close()
        # c nous qui ferme
        # sigterm
        # au debut, on verifie si le port est utilisé ==> warning et stop, correction message TOO HIGH, corriger le fait qu'on il pert, socket.close()
        # fermer les deux terminaux
        if DEBUG:
            print("taille reçue =", len(data), "octets")
        return correct_order, mode

    def play(self, cfd):
        self.client_request(cfd, 0)
        return 0

    @test
    def single_client_request(self, cfd):
        correct_order, mode = self.client_request(cfd, 1)
        if correct_order == 1 and DEBUG == 0:
            Warnings.append(
                "Warning! Majorant de l'intervalle >> minorant. Mode Debug -d vous donnera plus de details.")

        if mode != 2 and DEBUG == 0:
            Warnings.append(
                "Warning! Majorant de l'intervalle >> minorant. Mode Debug -d vous donnera plus de details.")

        if DEBUG:
            print("Result = ", end='')
        return cfd

    def handle_server(self):
        result = 0
        client_socket = t.connect_to_server(IP, PORT)
        try:
            self.client_request(client_socket, 1)
        except (AssertionError, FileNotFoundError, Exception, OSError, AttributeError) as e:
            print(str(e))
            result = 1
        return result

    @test
    def multiple_clients_test_interactive(self, n):
        threads = []
        result = 0
        for i in range(n):
            t = threading.Thread(target=self.handle_server)
            threads.append(t)
            t.start()
            result = self.handle_server()
        for thread in threads:
            thread.join()
        if result != 0:
            print("Result = ", end='')
            raise AssertionError

    def terminate_process_by_port(self, port):
        # Exemple écrit sur le terminal: $ lsof -t -i 53140
        command = f'lsof -t -i :{port}'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)  # Popen donne return code, mais subprocess.check_ouptut non
        output, error = process.communicate()  # similaire à check output pour Popen

        if process.returncode == 0:
            pid = int(output.decode().strip())
            subprocess.run(['kill', str(pid)])
            if DEBUG == 1:
                print(f"Server killed: {pid}")

    @test
    def test_too_high_too_low_lose(self, cfd):
        self.client_request(cfd, 2)
        return 0


    def create_msg(self, correct_number, received_guess):
        if received_guess == correct_number:
            if DEBUG ==1:
                print("YOU WIN!")
            return [WIN, correct_number]
        elif received_guess > correct_number:
            if DEBUG ==1:
                print("TOO HIGH!")
            return [TOO_HIGH, correct_number]
        elif received_guess < correct_number:
            if DEBUG ==1:
                print("TOO HIGH!")
            return [TOO_LOW, correct_number]

    def server_receive(self, cfd):
        sys.stdout.flush()
        data = cfd.recv(2)
        if len(data) == 0:
            if DEBUG == 1:
                print("Fin du test. Pas de données reçues")
            cfd.close()
            return "belle_fin"

        received_number = int.from_bytes(data, byteorder='big')
        received_number = received_number & 0xFF  # Mask to keep only the least significant byte
        if DEBUG == 1:
            print(f"number : {received_number}, Bytes: {data}")
        return received_number
        """
        try:
            guess = struct.unpack('ii', data)
            mode = 0
        except (SyntaxError, struct.error) as e:
            try:
                guess = struct.unpack('!H', data)[0]
                mode = 1
            except (SyntaxError, struct.error) as e:
                try:
                    guess = struct.unpack('!B', data)[0]
                    mode = 2
                except:
                    guess = struct.unpack('!B', data)
                    mode = 3
                    """
    @test
    def Guessing_Game_Interaction_Test(self, client_socket):
        mode = self.send_range(client_socket)
        number_to_guess = random.randrange(5, 120)
        print("Serveur reçoit 1 octet, envoie 2 octets (W/L/.., nombre_à_deviner)")
        print(f"number to guess: {number_to_guess} ")
        for i in range(NB_TRY):
            # handle incoming data
            guess = self.server_receive(client_socket)
            if guess == number_to_guess:
                print(f"YOU WIN! Guessed {number_to_guess}")
                guess = "belle_fin"
                break
            if DEBUG == 1:
                print(f"Received guess: {guess} ")
            msg_list = self.create_msg(number_to_guess, guess)
            client_socket.send((msg_list[0] & 0xFF).to_bytes(1, byteorder='big'))
            client_socket.send((msg_list[1] & 0xFF).to_bytes(1, byteorder='big'))
            """if number_to_guess == guess:
                client_socket.close()
                break"""

        if guess != "belle_fin":
            # if more than NB_TRY, LOOSING PART:
            client_socket.send((LOOSE & 0xFF).to_bytes(1, byteorder='big'))
            client_socket.send((number_to_guess & 0xFF).to_bytes(1, byteorder='big'))
            raise Exception("LOST!, Values [HIGH,LOW, WIN, LOSE] or number of tries may not be matching. -v to change values")
        print("Resultat du Guessing Game Interaction Test= ", end='')
        # close connection
        client_socket.close()
    @test
    def send_range(self, client_socket):

        lower_bound = 5
        upper_bound = 120

        try:
            client_socket.send(lower_bound.to_bytes(1, byteorder='big'))
            client_socket.send(upper_bound.to_bytes(1, byteorder='big'))
        except (SyntaxError, struct.error) as e:
            print("Error")

        return 0
    def intialise_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind à un port
        server_socket.bind(('', PORT))
        print("Port choisi: %d" % PORT)
        server_socket.listen(10)
        return server_socket
    @test
    def TEST_CLIENT_ETUDIANT(self, server_socket):
        # while True
        # accepte les nouvelles connections
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from %s:%d" % client_address)
        print("Test Launch OK")

        client_socket, client_address = server_socket.accept()
        print("Accepted connection from %s:%d" % client_address)
        self.Guessing_Game_Interaction_Test(client_socket)
        server_socket.close()
        print("Resultat du Test Client Etudiant= ", end='')
        t.kill_terminal()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test pour verifier le bon fonctionnement de votre TP')
    parser.add_argument('program_name', type=str, help='path de votre programme digest')
    parser.add_argument('port', type=int, help='port number for server connection')
    parser.add_argument('-i', '--ip_adress', type=str, help='prend une adresse ip comme agrument')
    parser.add_argument('-p', action='store_true', help='test toi même  les valeurs à envoyer au Serveur')
    parser.add_argument('-d', action='store_true',
                        help='DEBUGGING MODE: montre les donnèes reçues,envoyées,leurs tailles')
    parser.add_argument('-v', '--values', type=str,
                        help='choisir les valeurs High/Low/Win/lose comme liste: Exemple: [1,-1,0,-2]')
    parser.add_argument('try_number', type=int, help="nombre d essai pour LOSE, obligatoire pour le bon test de LOSE")
    parser.add_argument('-c', action='store_true',
                        help='Test Client, ./test name_client_program -c')

##options obligatoire number tests
    args = parser.parse_args()
    program_name = args.program_name
    PORT = args.port
    t = Test()
    NB_TRY = args.try_number
    print(bcolors.Magenta + "Try number changed to:" + bcolors.ENDC + f"\n{NB_TRY} tries ")

    if args.d:
        DEBUG = 1
    if args.values:
        values = args.values.strip('[]').split(',')
        TOO_HIGH = int(values[0])
        TOO_LOW = int(values[1])
        WIN = int(values[2])
        LOOSE = int(values[3])
        print(
            bcolors.Magenta + "Values changed to:" + bcolors.ENDC + f"\nTOO_HIGH={TOO_HIGH}, TOO_LOW={TOO_LOW}, WIN={WIN}, LOSE={LOOSE} ")
    if args.ip_adress:
        IP = args.ip_adress

    if t.check_port_in_use(PORT):
        print(bcolors.Magenta+ f"PORT {PORT} UTILISÉ." + bcolors.ENDC)
        print(f"Il faut attendre 60 secondes sur Linux pour que le port soit de nouveau accessible.L'état TIME-WAIT permet d'éviter que des segments en retard ne soient acceptés dans une connexion différente")
        PORT = t.generate_port()
        print(f"Nouveau Port: {PORT}")
    print(bcolors.Magenta + '--- BEGIN TEST ---\n' + bcolors.ENDC)
    if args.c:
        # Client Test
        server_client = t.intialise_server()
        launched_terminal = t.launch_program("client")
        t.TEST_CLIENT_ETUDIANT(server_client)
        print(bcolors.Magenta + '\n--- END TEST ---' + bcolors.ENDC)
    else:
        # Server Test
        launched_terminal = t.launch_program("server")
        client_socket = t.connect_to_server(IP, PORT)
        t.test_connect(client_socket)
        if args.p:
            # insert your own values test
            t.play(client_socket)
        else:
            # Autonomous
            t.single_client_request(client_socket)
            client_socket = t.connect_to_server(IP, PORT)
            t.test_too_high_too_low_lose(client_socket)
            t.multiple_clients_test_interactive(number_servers)
            t.print_warnings()
        print(bcolors.Magenta + '\n--- END TEST ---' + bcolors.ENDC)
        if DEBUG == 1:
            print(f"Terminal PID: {launched_terminal.pid}")
        t.kill_terminal()
        # t.terminate_process_by_port(PORT)

    # os.killpg(launched_terminal.pid, signal.SIGTERM)
# os.killpg(os.getpgid(0), signal.SIGTERM)
    sys.exit()
