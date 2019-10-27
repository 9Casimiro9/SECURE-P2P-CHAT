import pyfiglet
from colorama import Fore, Back, Style 

def generateBanner(text):

    ascii_banner = pyfiglet.figlet_format(text)
    print(Fore.MAGENTA + ascii_banner)
    print(Fore.WHITE)