
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

print(f"{bcolors.Blue}BEGIN TESTING{bcolors.ENDC}")
print(f"{bcolors.Green}TEST 1 OK{bcolors.ENDC}")
print(f"{bcolors.Red}Test 2 NOT OK : le hash_fichier() retourne des résultats incorrects. {bcolors.ENDC}")
print(f"{bcolors.Green}TEST 3 OK{bcolors.ENDC}")

