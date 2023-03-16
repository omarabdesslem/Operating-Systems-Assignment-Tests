import unittest
import subprocess  # shell interactions
import hashlib  # fonctions de hachage en Python, utilisées pour comparer l'output avec notre programme
import tempfile
import random
import base64
import os


program_name = "./digest"  # definir le nom voulu
n =2 #nombre de temp files/ taille du hash générés par test voulu

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

"""
def test():
    if __name__ == '__main__':
        test_failed = False
        if test_failed:
            print(bcolors.Red + "Some tests have failed." + bcolors.ENDC)
        else:
            print(bcolors.Green + "All tests have passed successfully!" + bcolors.ENDC)
"""



class Test_TP2(unittest.TestCase):

    #@test
    def test_string_hash(self):
        prg_name = "./digest"
        # Generate random bytes
        random_bytes = os.urandom(n)

        # encode en base64, étape nécessaire
        encoded_bytes = base64.b64encode(random_bytes)

        # Decode the base64-encoded bytes into a string
        input_string = encoded_bytes.decode('utf-8')
        hashed_input = hashlib.sha1(input_string.encode()).hexdigest().strip()
        output_string = subprocess.check_output([prg_name, str(input_string)], bufsize=4096).decode().replace('\n',
                                                                                                              '').replace(
            '(null)', '').strip()
        print(f"ouput string = {output_string}")
        expected_result = (hashed_input + " " + input_string).strip()
        print(f"expected is  = {expected_result}")
        a = self.assertEqual(output_string, expected_result)
        print(f"{bcolors.Green}TEST 1 OK {bcolors.ENDC}")
        #if expected_result in output_string:
            #raise AssertionError(f"Test Failed: \n{output_string} != {expected_result}")

    #@test
    def test_file_hash(self):
        list_of_files = [tempfile.NamedTemporaryFile(mode="w+", delete=False) for i in
                         range(n)]  # create list of temporary files
        input_string = [program_name, "-f"]
        expected_output = ""

        for fp in list_of_files:
            pathed_name = fp.name
            os.chmod(pathed_name, 0o777)
            input_string.append(pathed_name)  # line qu'on va tester
            # Generate 10 random bytes
            random_bytes = os.urandom(10)

            # Encode the random bytes in base64
            encoded_bytes = base64.b64encode(random_bytes)

            contenu = encoded_bytes
            expected_hash = hashlib.sha1(contenu).hexdigest()
            expected_output += f"{expected_hash} {pathed_name}\n"
            fp.write(encoded_bytes.decode('utf-8'))
            fp.close()  # fermer le fichier avant d'appeler subprocess.check_output
            # print("sony".encode('utf-8'))
            #print(f"expected output =   {expected_output}")
            # print(contenu.decode('utf-8'))
            print(f"Shell command: {' '.join(input_string)}")
            resultat = subprocess.check_output(input_string, bufsize=4096).decode().replace('(null)', '')
            print(f"{bcolors.Blue}Expected output:\n{bcolors.ENDC}{expected_output}")
            print(f"{bcolors.Blue}Result:\n{bcolors.ENDC}{resultat}")
            a = self.assertEqual(resultat, expected_output)
            # if resultat != expected_hash:
            #    raise AssertionError(
            # f'Expected hash of {input_string} and result are not identical\n Expected {expected_output}')
            # print("test_file_hash OK")
        print(f"{bcolors.Green}TEST 2 OK {bcolors.ENDC}")

        for fp in list_of_files:
            os.unlink(fp.name)
    #@test
    def test_string_hash_md5(self):
        prg_name = "./digest"
        # Generate 10 random bytes
        random_bytes = os.urandom(n)

        # Encode the random bytes in base64
        encoded_bytes = base64.b64encode(random_bytes)

        # Decode the base64-encoded bytes into a string
        input_string = encoded_bytes.decode('utf-8')
        hashed_input = hashlib.md5(input_string.encode()).hexdigest()
        output_string = subprocess.check_output([prg_name, str(input_string), "-t", "md5"],
                                                bufsize=4096).decode().replace('\n', '').replace(
            '(null)', '')
        expected_result = (hashed_input + " " + input_string).strip()
        a = self.assertEqual(output_string, expected_result)
        print(output_string)
        print(expected_result)
        print(f"{bcolors.Green}TEST 3 OK {bcolors.ENDC}")
         
    #@test
    def test_file_hash_md5(self):
        list_of_files = [tempfile.NamedTemporaryFile(mode="w+", delete=False) for i in
                            range(n)]  # create list of temporary files
        input_string = [program_name, "-f", "-t", "md5"]
        expected_output = ""
        
        for fp in list_of_files:
            pathed_name = fp.name
            os.chmod(pathed_name, 0o777)
            input_string.append(pathed_name)  # line qu'on va tester
            # Generate 10 random bytes
            random_bytes = os.urandom(10)
            input_string.remove("-t")
            input_string.remove("md5")
            # Encode the random bytes in base64
            encoded_bytes = base64.b64encode(random_bytes)

            contenu = encoded_bytes
            expected_hash = hashlib.md5(contenu).hexdigest()
            expected_output += f"{expected_hash} {pathed_name}\n"
            fp.write(encoded_bytes.decode('utf-8'))
            fp.close()  # fermer le fichier avant d'appeler subprocess.check_output
            # print("sony".encode('utf-8'))
            # print(f"expected output =   {expected_output}")
            # print(contenu.decode('utf-8'))
            input_string.append("-t")
            input_string.append("md5")
            print(f"Shell command: {' '.join(input_string)}")
            resultat = subprocess.check_output(input_string, bufsize=4096).decode().replace('(null)', '')
            print(f"{bcolors.Blue}Expected output:\n{bcolors.ENDC}{expected_output}")
            print(f"{bcolors.Blue}Result:\n{bcolors.ENDC}{resultat}")
            a = self.assertEqual(resultat, expected_output)
            # if resultat != expected_hash:
            #    raise AssertionError(
            # f'Expected hash of {input_string} and result are not identical\n Expected {expected_output}')
            # print("test_file_hash OK")
        print(f"{bcolors.Green}TEST 4 OK {bcolors.ENDC}")


t = Test_TP2()
t.test_string_hash()
t.test_file_hash()
t.test_string_hash_md5()
t.test_file_hash_md5()



