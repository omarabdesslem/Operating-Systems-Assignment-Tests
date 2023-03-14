import unittest
import subprocess  # shell interactions
import hashlib  # fonctions de hachage en Python, utilisées pour comparer l'output avec notre programme
import tempfile
import random
import base64
import os

# TODO: créer un tempfile et le tester avec test_file_hash(), créer une boucle pour tester le programme avec n tempfiles

program_name = "./digest"  # definir le nom voulu


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


class Test_TP2(unittest.TestCase):

    def test_string_hash(self):
        prg_name = "./digest"
        # Generate 10 random bytes
        random_bytes = os.urandom(10)

        # Encode the random bytes in base64
        encoded_bytes = base64.b64encode(random_bytes)

        # Decode the base64-encoded bytes into a string
        input_string = encoded_bytes.decode('utf-8')
        hashed_input = hashlib.sha1(input_string.encode()).hexdigest()
        output_string = subprocess.check_output([prg_name, str(input_string)], bufsize=4096).decode().replace('\n',
                                                                                                              '').replace(
            '(null)', '')
        expected_result = (hashed_input + " " + input_string).strip()
        a = self.assertNotEqual(output_string, expected_result)
        if output_string in expected_result:
            raise AssertionError(f"Test Failed: \n{output_string} != {expected_result}")

    def test_file_hash(self):
        list_of_files = [tempfile.NamedTemporaryFile(mode="w+", delete=False) for i in range(10)]  # create list of temporary files
        input_string = [program_name, "-f"]
        expected_output = ""
        for fp in list_of_files:
            pathed_name = fp.name
            os.chmod(pathed_name, 0o777)
            input_string.append(pathed_name) # line qu'on va tester
            # Generate 10 random bytes
            random_bytes = os.urandom(10)

            # Encode the random bytes in base64
            encoded_bytes = base64.b64encode(random_bytes)

            contenu = encoded_bytes
            expected_hash = hashlib.sha1(contenu).hexdigest()
            expected_output += f"{expected_hash} {pathed_name}\n"
            fp.write("chips")
            fp.close()  # fermer le fichier avant d'appeler subprocess.check_output
            result_1 = subprocess.check_output(["cat", pathed_name])
            print(result_1)
            #print("sony".encode('utf-8'))
            #print(f"expected output =   {expected_output}")
            #print(contenu.decode('utf-8'))
            print(input_string)
            # Ajouter les permissions de lecture pour l'utilisateur courant

            resultat = subprocess.check_output(input_string, bufsize=4096).decode().replace('(null)', '')
            print(resultat)
            #a = self.assertEqual(resultat, expected_output)
            #if resultat != expected_hash:
            #    raise AssertionError(
                    #f'Expected hash of {input_string} and result are not identical\n Expected {expected_output}')
            #print("test_file_hash OK")

        for fp in list_of_files: fp.close()


t = Test_TP2()
t.test_string_hash()
t.test_file_hash()
