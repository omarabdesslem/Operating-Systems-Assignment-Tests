import unittest
import subprocess #shell interactions
import hashlib	  #fonctions de hachage en Python, utilisées pour comparer l'output avec notre programme
import tempfile
import random
#TODO: créer un tempfile et le tester avec test_file_hash(), créer une boucle pour tester le programme avec n tempfiles

program_name = "./digest" #definir le nom voulu


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
        self.FAIL = ''
        self.ENDC = ''

class Test_TP2(unittest.TestCase):

	def test_string_hash(self):
		    input_string = "sony\n"
		    expected_output = hashlib.sha1(input_string.encode()).hexdigest()
		    resultat = subprocess.check_output([program_name, input_string.encode()], bufsize=4096).decode().replace('\n', '').replace('(null)', '')
		    print("(will be removed)result from shell =",resultat)
		    expected_hash = expected_output + "  " + input_string
		    print("(will be removed)expected output =",expected_hash)
		    a = self.assertEqual(resultat, expected_hash)
		    if (resultat!=expected_hash): 
		    	raise AssertionError(f'Expected hash of {input_string} and result are not identical\n Expected {expected_hash}')
		    print("test_string_hash OK")
		    
	def test_file_hash(self):

		input_string = "-f "
		for n in range(50):
			f = tempfile.NamedTemporaryFile()
			input_string += f.path + "/"+ f.name

		random_sequence=random.getrandbits(100)
		input_string= "-f " + fichier	#line qu'on va tester
		expected_output = hashlib.sha1(random_sequence).hexdigest()
		print("(will be removed)expected output =",expected_hash)
		resultat = subprocess.check_output([program_name, input_string.encode()], bufsize=4096).decode().replace('\n', '').replace('(null)', '')
		print({bcolors.Magenta}"(will be removed)result from shell =",resultat{bcolors.endc})
		a = self.assertEqual(resultat, expected_hash)
		if (resultat!=expected_hash): 
		    	raise AssertionError(f'Expected hash of {input_string} and result are not identical\n Expected {expected_hash}')
		print("test_file_hash OK")

	    	
t = Test_TP2()
t.test_string_hash()
t.test_file_hash()

