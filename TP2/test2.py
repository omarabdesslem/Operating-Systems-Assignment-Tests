#!/usr/bin/env python3

import unittest
import subprocess
import hashlib
import tempfile
import random
import base64
import os
import sys
import logging
import argparse

file_number = 2
hash_length = 5


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

def check(expected_hash, resultat):
    if expected_hash not in resultat:
        raise AssertionError(f'Expected hash of {expected_hash} and result are not identical{resultat}\n')


def test(func):
    def wrapper(self):
        global test_failed
        print(func.__name__ + ": ", end="")
        try:
            func(self)
        except AssertionError or FileNotFoundError or AttributeError as e:
            print(bcolors.Red + "FAILED" + bcolors.ENDC)
            print(str(e))
            test_failed = True
        else:
            print(bcolors.Green + "SUCCESS" + bcolors.ENDC)

    return wrapper



class Test(unittest.TestCase):
    def hash_string_compare(self, hash_type):
        random_bytes = os.urandom(hash_length)
        encoded_bytes = base64.b64encode(random_bytes) #convertir en ascii en utilisant la base 64, étape necessaire
        random_string = encoded_bytes.decode('utf-8') #convertir l'object en octets en string avec decode
        if hash_type == 'md5':
            input_string = [program_name, str(random_string), "-t", "md5"]
            hashed_input = hashlib.md5(random_string.encode()).hexdigest()
        else:
            hashed_input = hashlib.sha1(random_string.encode()).hexdigest()
            input_string = [program_name, str(random_string)]
        output_string = subprocess.check_output(input_string,
                                                bufsize=4096).decode()
        check(hashed_input, output_string)

    def hash_file_compare(self, hash_type):
        list_of_files = [tempfile.NamedTemporaryFile(mode="w+", delete=False) for i in
                         range(file_number)]  # create list of temporary files
        expected_output = ""
        if hash_type == 'md5':
            input_string = [program_name, "-f", "-t", "md5"]
        else:
            input_string = [program_name, "-f"]
        for fp in list_of_files:
            pathed_name = fp.name
            os.chmod(pathed_name, 0o777)
            input_string.append(pathed_name)  # line qu'on va tester
            random_bytes = os.urandom(hash_length)
            if hash_type == 'md5':
                input_string.remove("-t")
                input_string.remove("md5")
            # Encode the random bytes in base64 ==> letters/symbols
            contenu = base64.b64encode(random_bytes)
            if hash_type == 'md5':
                expected_hash = hashlib.md5(contenu).hexdigest()
            else:
                expected_hash = hashlib.sha1(contenu).hexdigest()
            fp.write(contenu.decode('utf-8'))  # ecrit contenu dans le fichier
            fp.close()  # fermer le fichier avant d'appeler subprocess.check_output
            if hash_type == 'md5':
                input_string.append("-t")
                input_string.append("md5")
            resultat = subprocess.check_output(input_string, bufsize=4096).decode()
            check(expected_hash, resultat)
        for fp in list_of_files:
            os.unlink(fp.name)

    @test
    def test_string_hash(self):
        self.hash_string_compare("sha1")

    @test
    def test_file_hash(self):
        self.hash_file_compare("sha1")

    @test
    def test_string_hash_md5(self):
        self.hash_string_compare("md5")

    @test
    def test_file_hash_md5(self):
        self.hash_file_compare("md5")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        program_name = sys.argv[1]
        argument_type = sys.argv[2]
        t = Test()
        if argument_type == "sha1":
            print(bcolors.Blue + '--- BEGIN TEST ---\n' + bcolors.ENDC)
            print(bcolors.Blue + '--- TESTING STRING_HASH ---' + bcolors.ENDC)
            t.test_string_hash()
            print(bcolors.Blue + '--- TESTING FILE_HASH ---' + bcolors.ENDC)
            t.test_file_hash()
            print(bcolors.Blue + '\n--- END TEST ---' + bcolors.ENDC)

        else:
            if argument_type == "md5":
                print(bcolors.Blue + '--- BEGIN TEST ---\n' + bcolors.ENDC)
                print(bcolors.Blue + '--- TESTING STRING_HASH ---' + bcolors.ENDC)
                t.test_string_hash()
                print(bcolors.Blue + '--- TESTING FILE_HASH ---' + bcolors.ENDC)
                t.test_file_hash()
                print(bcolors.Blue + '\n--- END TEST ---' + bcolors.ENDC)

            else:
                print("Test requires valid hash type")
    else:
        print("Test requires program name. Example: Digest")
        print("Test requires valid hash type")

