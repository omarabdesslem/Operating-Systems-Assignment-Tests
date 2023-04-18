#!/usr/bin/env python3

import subprocess
import hashlib
import tempfile
import base64
import os
import sys
import argparse

##valeurs par defaults
file_number = 3
hash_length = 5
delete_value = True


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
    def check(self, input_string, resultat):
        output_string = subprocess.check_output(input_string, bufsize=4096).decode()
        file_hash = output_string.split()[0] #utile si plusieurs lignes reçues
        if file_hash not in resultat:
            if resultat not in file_hash:
                raise AssertionError(f"output:\n{output_string}\ndifferent from expected:\n{resultat}\n")

    @test
    def hash_string_compare(self, hash_type):
        random_string = base64.b64encode(os.urandom(hash_length)).decode('utf-8')
        if hash_type == 'md5':
            input_string = [program_name, str(random_string), "-t", "md5"]
            hashed_input = hashlib.md5(random_string.encode()).hexdigest()
        else:
            hashed_input = hashlib.sha1(random_string.encode()).hexdigest()
            input_string = [program_name, str(random_string)]
        self.check(input_string, hashed_input)

    @test
    def hash_file_compare(self, hash_type, chosen_number_files):
        list_of_files = [tempfile.NamedTemporaryFile(mode="w+", delete=delete_value) for i in
                         range(chosen_number_files)]  # create list of temporary files
        input_string = [program_name, "-f"]
        expected_hash = ""
        for fp in list_of_files:
            pathed_name = fp.name
            input_string.append(pathed_name)  # line qu'on va tester
            contenu = base64.b64encode(os.urandom(hash_length))  # Encode the random bytes in base64 ==> letters/symbols
            if hash_type == 'md5':
                expected_hash += hashlib.md5(contenu).hexdigest() + " "
            else:
                expected_hash += hashlib.sha1(contenu).hexdigest() + " "
            fp.write(contenu.decode('utf-8'))  # ecrit contenu dans le fichier
            fp.flush()
            if hash_type == 'md5':
                input_string.append("-t")
                input_string.append("md5")
            self.check(input_string, expected_hash)

        for fp in list_of_files:
            fp.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test pour verifier le bon fonctionnement de votre TP: Hash Digest')
    parser.add_argument('program_name', type=str, help='path de votre programme digest')
    parser.add_argument('-f', '--file_number', type=int, help='nombre de fichiers utilisé, 3 par default')
    parser.add_argument('-c', '--string_size', type=int,
                        help='taille de la chaîne de caractères generée, par default 5 max 64000')
    parser.add_argument('-k', action='store_true', help='garde les fichiers temporaires')
    args = parser.parse_args()
    program_name = args.program_name
    if args.file_number:
        file_number = args.file_number
    if args.string_size:
        hash_length = args.string_size
    if args.k:
        print("les fichiers temporaires seront gardés\n")
        delete_value = False
    t = Test()
    print(bcolors.Magenta + '--- BEGIN TEST ---\n' + bcolors.ENDC)
    print(bcolors.Blue + '--- TESTING STRING_HASH ---' + bcolors.ENDC)
    t.hash_string_compare("sha1")
    print(bcolors.Blue + '--- TESTING MD5 STRING_HASH ---' + bcolors.ENDC)
    t.hash_string_compare("md5")
    print(bcolors.Blue + '\n--- TESTING FILE_HASH ---' + bcolors.ENDC)
    t.hash_file_compare("sha1", 1)
    print(bcolors.Blue + '--- TESTING MD5 FILE_HASH ---' + bcolors.ENDC)
    t.hash_file_compare("md5", 1)
    print(bcolors.Blue + '\n--- TESTING MULTIPLE FILE_HASH ---' + bcolors.ENDC)
    t.hash_file_compare("sha1", file_number)
    print(bcolors.Blue + '--- TESTING MD5 MULTIPLE FILE_HASH  ---' + bcolors.ENDC)
    t.hash_file_compare("md5", 5)
    print(f'\nle nombre de fichiers est {file_number}, la taille des chaines est {hash_length} octets')
    print(bcolors.Magenta + '--- END TEST ---' + bcolors.ENDC)
