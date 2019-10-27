import os
import time

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from base64 import b64decode, b64encode


key = RSA.generate(2048)
debug = False
key_dir = "key/"
delay_time = 1.5

try:
    os.stat(key_dir)
except:
    os.mkdir(key_dir) 

class PrivateKey:

    __private_key = ""
    __key_dir = key_dir


    def __init__(self, chosenDebug, username):
        debug = chosenDebug

        if not debug:
            delay_time = 0

        self.__key_dir += username + "/"

        try:
            os.stat(self.__key_dir)
        except:
            os.mkdir(self.__key_dir) 

        try:
            open(self.__key_dir + "private.pem")
            
            if debug:
                time.sleep(delay_time)
                print("Private key already exists! Loading saved key")
        
            self.__get_private_key_from_file()
        
        except:
            if debug:
                time.sleep(delay_time)
                print("Generating private key")

            self.__generate()
            
    def __generate(self):
        self.__private_key = key.export_key()
        file_out = open(self.__key_dir + "private.pem", "wb")
        file_out.write(self.__private_key)

        if debug:
            time.sleep(delay_time)
            print(self.__private_key)
            time.sleep(delay_time)
            print("Private key generated")

    def __get_private_key_from_file(self):
        pem_file = open(self.__key_dir + 'private.pem','r')
        self.__private_key = pem_file.read()

        if debug:
            time.sleep(delay_time)
            print(self.__private_key)
            time.sleep(delay_time)
            print("Private key loaded")
        
    def decrypt(self, ciphertext):
        privKeyObj = RSA.importKey(self.__private_key)
        cipher = PKCS1_OAEP.new(privKeyObj)
        message = cipher.decrypt(ciphertext).decode("utf-8")
        return message

    def decryptv2(self, ciphertext):
        privKeyObj = RSA.importKey(self.__private_key)
        raw_cipher_data = b64decode(ciphertext)
        message = privKeyObj.decrypt(raw_cipher_data)
        return message

class PublicKey: 

    __public_key = ""
    __key_dir = key_dir

    def __init__(self, chosenDebug, username):
        debug = chosenDebug

        if not debug:
            delay_time = 0

        self.__key_dir += username + "/"

        if debug:
            print(self.__key_dir)
        
        try:
            os.stat(self.__key_dir)
        except:
            os.mkdir(self.__key_dir) 

        try:
           
            open(self.__key_dir + "public.pem")

            if debug:
                time.sleep(delay_time)
                print("Public key already exists! Loading saved key")
            
            self.__get_public_key_from_file()
            
        except Exception as e:
            if debug:
                time.sleep(delay_time)
                print("Generating public key")

            self.__generate()

    def get_key(self):
        try:
            return self.__public_key.replace("\n","")
        except:
            return self.__public_key

    def get_public_key(self):
        return self.__public_key
           
    def __generate(self):
        self.__public_key = key.publickey().export_key()
        file_out = open(self.__key_dir + 'public.pem', 'wb')
        file_out.write(self.__public_key)

        if debug:
            time.sleep(delay_time)
            print(self.__public_key)
            time.sleep(delay_time)
            print("Public key generated")

    def __get_public_key_from_file(self):
        pem_file = open(self.__key_dir + 'public.pem','r')
        self.__public_key = pem_file.read()

        if debug:
            time.sleep(delay_time)
            print(self.__public_key)
            time.sleep(delay_time)
            print("Public key loaded")
    
    def encrypt(self, message, public_key):
        message = message.encode("utf-8")
        pubKeyObj =  RSA.importKey(public_key)
        cipher = PKCS1_OAEP.new(pubKeyObj)
        ciphertext = cipher.encrypt(message)
        return ciphertext


    def encryptv2(self, message, publickey):
        message = message.encode("utf-8")
        pubKeyObj =  RSA.importKey(self.__public_key)
        cipher = PKCS1_OAEP.new(pubKeyObj)
        ciphertext = cipher.encrypt(message)
        ciphertext = b64encode(ciphertext)
        return ciphertext


    def format(self, public_key):
        if debug:
            print(public_key)
        try:
            RSA.importKey(public_key.replace("\n",""))
            return public_key.replace("\n","")
        except:
            length = 26
            pbk = public_key[:length] + "\n"
            for count in range(6):
                i = count + 1
                pbk += public_key[length:length + 64] + "\n"
                length = 26 + (64 * (i))
            pbk += public_key[-((24) + 8):-(24)] + "\n"
            pbk += public_key[-24:]
            return pbk

if debug:
    username = "vm1"
    pbk = PublicKey(username)
    prk = PrivateKey(username)
    print(pbk.format(pbk.get_key()))
    
    message = str(input("Insert the message that you want to encrypt : \n"))
    cipher = pbk.encrypt(message,pbk.format(pbk.get_key()))
    message = prk.decrypt(cipher)

    print(("=" * 15) + "OUTPUT" + ("=" * 15))
    print("Cipher text:")
    print(cipher)
    print("Message:")
    print(message)
