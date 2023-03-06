import unittest
import subprocess #shell interactions
import hashlib	  #fonctions de hachage en Python, utilisées pour comparer l'output avec notre programme
import tempfile
#TODO: créer un tempfile et le tester avec test_file_hash(), créer une boucle pour tester le programme avec n tempfiles

program_name = "./digest" #definir le nom voulu


class Test_TP2(unittest.TestCase):

	def test_string_hash(self):
		input_string="Windows 7"
		expected_output = hashlib.sha1(input_string)
		resultat = subprocess.run([program_name, input_string], check_output=True) #execute la commande de test dans le chell, renvoi l'output dans stdout, créer une classe subprocess stockée dans le résultat
		a = self.assertEqual(res.stdout.decode(sys.stdout.encoding).strip(), expected_output + "  " + input_string) #converts stdout de bstring en string, strips le \n , compare les deux strings avec assertEqual
		if(a): printf(" String HASH OK\n")

	def test_file_hash(self):
		fichier = "fichier1.txt" 	#va être remplacer avec tempfile
		input_string= "-f " + fichier	#line qu'on va tester
		expected_output = hashlib.sha1(open(fichier)) #hashing du fichier
		resultat = subprocess.run([program_name, input_string], check_output=True)
		a = self.assertEqual(res.stdout.decode(sys.stdout.encoding).strip(), expected_output + "  " + input_string")
		if(a): printf(" FILE HASH OK\n")

	def test_md5(self):
		#TODO

t = Test()
t.test_string_hash()

