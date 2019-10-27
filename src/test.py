import sys
import time

from collections import OrderedDict
from classes import JsonWEncryption
from cryptogen import PrivateKey, PublicKey
import base64

debug = False

class ProgressBar:

    __count = 0
    __progressPerExec = 0
    __times = 0

    def __init__(self, times):
        self.__times = times
        self.__progressPerExec = 100 / times
        print("[" + (" " * 100) + "]" + "0%")

    def progressOnce(self):
        sys.stdout.write("\033[F")
        self.__count += 1
        progress = int(self.__count * self.__progressPerExec)
        out = "["
        out += "=" * progress
        if progress != 100:
            out += ">"
        out += " " * (100 - progress)
        if progress != 100:
            out = out[:-1]
        out += "]" 
        out += str(progress) + "%"

        time.sleep(0.5)

        print(out)

    def progress(self):

        for count in range(101):
            sys.stdout.write("\033[F")
            i = count + 1
            out = "["
            out += "=" * count
            if count != 100:
                out += ">"
            out += " " * (100 - count)
            
            out += "]" 
            out += str(count) + "%"

            time.sleep(0.05)

            print(out)        

        print("COMPLETE!!!")


def testLines():

    print("something")

    sys.stdout.write("\033[F")

    print("else also else")

def dic():
    s = "123456"

    #s[-1] = ""

    print(s[:-1])

'''
times = 5

pb = ProgressBar(times)

for i in range(times):
    pb.progressOnce()

'''
username = "vm1"
pb = PublicKey(username)
print(pb.get_key())
print(pb.format(pb.get_key()))
exit()

cipher = pb.encrypt("hello",pb.format(pb.get_key()))
print(cipher)
print(type(cipher))
cipher = cipher.decode('unicode-escape')
print(cipher)
print(type(cipher))
cipher = cipher.encode('ISO-8859-1')
print(cipher)
print(type(cipher))



pr = PrivateKey(username)


jwe = JsonWEncryption(False, '{"package": {"IP": "192.168.0.2","username": "vm1","message": "hi","target": "192.168.0.4"}}')


print(pr.decrypt(cipher))

print(jwe.sender)