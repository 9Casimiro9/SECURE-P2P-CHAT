import os
import time

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

key = RSA.generate(2048)
debug = True
key_dir = "key/"

try:
    os.stat(key_dir)
except:
    os.mkdir(key_dir) 

class PrivateKey:

    __private_key = ""

    def __init__(self):
        try:
            open(key_dir + "private.pem")
            
            if debug == True:
                time.sleep(1.5)
                print("Private key already exists! Loading saved key")
        
            self.__get_private_key_from_file()
        
        except:
            if debug == True:
                time.sleep(1.5)
                print("Generating private key")

            self.__generate()
            
    def __generate(self):
        self.__private_key = key.export_key()
        file_out = open(key_dir + "private.pem", "wb")
        file_out.write(self.__private_key)

        if debug == True:
            time.sleep(1.5)
            print(self.__private_key)
            time.sleep(1.5)
            print("Private key generated")

    def __get_private_key_from_file(self):
        pem_file = open(key_dir + 'private.pem','r')
        self.__private_key = pem_file.read()

        if debug == True:
            time.sleep(1.5)
            print(self.__private_key)
            time.sleep(1.5)
            print("Private key loaded")
        
    def decrypt(self, ciphertext):
        privKeyObj = RSA.importKey(self.__private_key)
        cipher = PKCS1_OAEP.new(privKeyObj)
        message = cipher.decrypt(ciphertext).decode("utf-8")
        return message

class PublicKey: 

    __public_key = ""

    def __init__(self):
        try:
            open(key_dir + "public.pem")

            if debug == True:
                time.sleep(1.5)
                print("Public key already exists! Loading saved key")
            
            self.__get_public_key_from_file()
            
        except Exception as e:
            if debug == True:
                time.sleep(1.5)
                print("Generating public key")

            self.__generate()

    def get_key(self):
        return self.__public_key.replace("\n","")
           
    def __generate(self):
        self.__public_key = key.publickey().export_key()
        file_out = open(key_dir + 'public.pem', 'wb')
        file_out.write(self.__public_key)

        if debug == True:
            time.sleep(1.5)
            print(self.__public_key)
            time.sleep(1.5)
            print("Public key generated")

    def __get_public_key_from_file(self):
        pem_file = open(key_dir + 'public.pem','r')
        self.__public_key = pem_file.read()

        if debug == True:
            time.sleep(1.5)
            print(self.__public_key)
            time.sleep(1.5)
            print("Public key loaded")
    
    def encrypt(self, message):
        message = message.encode("utf-8")
        pubKeyObj =  RSA.importKey(self.__public_key)
        cipher = PKCS1_OAEP.new(pubKeyObj)
        ciphertext = cipher.encrypt(message)
        return ciphertext

    def format(self):
        try:
            RSA.importKey(self.__public_key.replace("\n",""))
        except:
            lengh = 26
            self.__public_key = self.__public_key[:lengh] + "\n" + self.__public_key[lengh:-lengh] + "\n" + self.__public_key[-(lengh - 2):]

if debug == True:

    pbk = PublicKey()
    prk = PrivateKey()
    
    message = str(input("Insert the message that you want to encrypt : \n"))
    cipher = pbk.encrypt(message)
    message = prk.decrypt(cipher)

    print(("=" * 15) + "OUTPUT" + ("=" * 15))
    print("Cipher text:")
    print(cipher)
    print("Message:")
    print(message)
