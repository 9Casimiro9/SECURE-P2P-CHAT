import json
import socket
import sys
import threading
import os

from client import Client
from generateSysData import Node
from classes import ProgressBar,JsonWEncryption

debug = False

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    __connections = []
    __clients = []
    running = True

    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)
        print("Server is online!")
        print("shutdown or exit to stop the server")

        if debug:
            print("startup len list")
            print(len(self.__connections))
            print(len(self.__clients))

        cThread = threading.Thread(target=self.command_input, args=())
        cThread.daemon = True
        cThread.start()

    def command_input(self):
        node = Node()
        i = input("> ")
        if i == "exit" or i == "shutdown":
            print("Stoping Server...")
            self.sock.close()            
            self.running = False
            exit()

        elif i == "help":
            commandsAvailableStr = ("-" * 10) + "LIST OF COMMANDS AVAILABLE" + ("-" * 10)
            print(commandsAvailableStr)
            print("connections")
            print("clients")
            print("clientsKeys")
            print("jsonClients")
            print("cls or clear")
            print("-" * len(commandsAvailableStr))

        elif i == "connections":
            node.outputConnections(self.__connections, self.__clients)

        elif i == "clients":
            node.outputClients(self.__clients)

        elif i == "clientsKeys":
            node.outputClientsKeys(self.__clients)

        elif i == "jsonClients":
            print(self.generateJsonClients(None))
        
        elif i == "cls" or i == "clear":
            try:
                os.system('clear')
            except:
                os.system('cls')

        else:
            sys.stdout.write("\033[F")
            print(i + ": command not found")
            print("List of commands available : 'help'")
        
        self.command_input()

    def handler(self, c, a):
        while self.running:
            data = c.recv(1024)
            data = data.decode("utf-8")

            if debug:
                print("data")
                print(data)

            try:
                jsonAuth = json.loads(data)["auth"]

                if debug:
                    print()
                    sys.stdout.write("\033[F")
                    print("auth")
                    print("authentication for : " + jsonAuth["username"] + " in progress...")

                ip = jsonAuth["ip"]
                username = jsonAuth["username"]
                publicKey = jsonAuth["publicKey"]

                client = Client(jsonAuth['ip'], jsonAuth["username"], jsonAuth["publicKey"])
                    
                try:
                    self.__clients.append(client)
                    if len(self.__clients) > 1:
                        self.sendAuthData()
                    if debug:
                        print(username + " authenticated")
                    else:
                        print()
                        sys.stdout.write("\033[F")
                        print(username + ' connected')
                except Exception as e:
                    print("An error as occurred doing the authentication for : " + username)
                    self.__connections.remove(c)
                    self.__clients.remove(client)

                if debug:
                    print("auth len list")
                    print(len(self.__connections))
                    print(len(self.__clients))
                
            except Exception as e:
                if debug:
                    print("no auth")
                    print(e)
                try:
                    json.loads(data)["package"]

                    if debug:
                        print("package")

                    for connection in self.__connections:
                        jsonMsg = json.loads(data)["package"]
                        sender = str(jsonMsg["IP"].replace(" ", ""))
                        connectionIP = str(connection.getpeername()[0])

                        print("connections output")
                        print("-" + sender + "-")
                        print("-" + connectionIP + "-")

                        if(sender != connectionIP):
                            connection.send(bytes(data, 'utf-8'))
                            print(data)
                            break
                
                except:
                    if debug:
                        print("no package")
                    
                    jwe = JsonWEncryption(debug,data)
                    target = jwe.target

                    for connection in self.__connections:
                        if debug:
                            print("checking for target " + target + " = " + str(connection.getpeername()[0]))

                        if(target == str(connection.getpeername()[0])):
                            try:
                                connection.send(bytes(data, 'utf-8'))
                                print("successfully routed the message from " + jwe.sender + " to " + target)
                            except Exception as e:
                                print("An  error as occurred routing the message from " + jwe.sender + " to " + target)
                            
    
                    try:
                        if not data:

                            if debug:
                                print("beg disconnected len list")
                                print(len(self.__connections))
                                print(len(self.__clients))

                            print(str(a[0]) + ':' + str(a[1]) + 'disconnected')
                            self.__connections.remove(c)
                            count = 0
                            for client in self.__clients:
                                if client.getIp() == a[0]:
                                    break
                                count += 1
                            del self.__clients[count]
                            c.close()

                            if debug:
                                print("disconnected len list")
                                print(len(self.__connections))
                                print(len(self.__clients))
                    except:
                        print("not data error")

                        

    def run(self):
        while self.running:
            c, a = self.sock.accept()

            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()

            self.__connections.append(c)
            #self.__connections[-1].send(bytes(self.generateJsonClients(), 'utf-8'))
            if debug:
                print()
                sys.stdout.write("\033[F")
                print(str(a[0]) + ':' + str(a[1]) + ' connected')

            if debug:
                print("connected len list")
                print(len(self.__connections))
                print(len(self.__clients))

        print("Server is now offline")
        exit()

    def sendAuthData(self):
        try:
            if debug:
                print(self.generateJsonClients("10.10.10.10"))
            print("sending auth data to all clients")
            pb = ProgressBar(len(self.__clients), debug)
            for client in self.__clients:
                for connection in self.__connections:
                    if debug:
                        print(connection.getpeername()[0] + " == " + client.getIp())
                    if str(connection.getpeername()[0]) == str(client.getIp()):
                        try:
                            connection.send(bytes(self.generateJsonClients(connection.getpeername()[0]), 'utf-8'))
                        finally:
                            #print(self.generateJsonClients(connection.getpeername()[0]))
                            pb.progressOnce()
                            if debug:
                                print("new connection")
                            break
                        

        except Exception as e:
            if debug:
                print("sendAuthData error: ")
                print(e)
        



    def generateJsonClients(self, receiver):
        #TODO: add the nodes to json
        if debug:
            print(receiver)
        jsonData = '{'
        jsonData += '"clients": ['
        i = 1
        for client in self.__clients:
            if debug:
                print("checking if " + receiver + " = " + client.getIp())
            if receiver != None and client.getIp() == receiver:
                if debug:
                    print("True")
                if len(self.__clients) == i:
                    jsonData = jsonData[:-1]
                continue
            jsonData += '{"Username": "' + client.getUsername() + '",'
            jsonData += '"IP": "' + client.getIp() + '",'
            jsonData += '"PublicKey": "' + client.getPublicKey().replace("\n","") + '"'
            jsonData += '}'
            if i != (len(self.__clients) - 1):
                jsonData += ','
                i += 1
        jsonData += ']'
        jsonData += '}'
    
        if debug:
            print(jsonData)

        return jsonData

    def createAuthJson(self):
	    jsonData = '{'
	    jsonData += '"auth": {'
	    jsonData += '"ip": "' + self.__ip + '",'
	    jsonData += '"username": "' + self.__username + '",'
	    jsonData += '"publicKey": "' + self.__publicKey.get_key() + '"'
	    jsonData += '}'
	    jsonData += '}'

	    if debug:
		    print(jsonData)
		
	    return jsonData

try:
	os.system('clear')
except:
	os.system('cls')

server = Server()
server.run()
