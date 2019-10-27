from Crypto.PublicKey import RSA

class Client:

    __ip = ""
    __username = ""
    __publicKey = ""


    def __init__(self, ip, username, publicKey):
        self.__ip = ip
        self.__username = username
        self.__publicKey = publicKey

    def getIp(self):
        return self.__ip
        
    def getUsername(self):
        return self.__username

    def getPublicKey(self):
        return self.__publicKey
    
