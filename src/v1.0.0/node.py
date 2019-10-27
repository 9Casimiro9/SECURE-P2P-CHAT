import socket
import threading
import sys
import json

debug = True

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    connections = []
    clients = dict()
    running = True

    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)
        print("Server is online!")
        print("Write exit or exit() to shutdown the server")

        cThread = threading.Thread(target=self.command_input, args=())
        cThread.daemon = True
        cThread.start()

    def command_input(self):
        i = input("")
        if i == "exit" or i == "exit()":
            print("Stoping Server...")
            self.sock.close()            
            self.running = False
            exit()

        else:
            print("Unknown command!")
            self.command_input()

    def handler(self, c, a):
        while self.running:
            data = c.recv(1024)
            data = data.decode("utf-8")
            try:
                jsonAuth = json.loads(data)["auth"]

                print("authentication for : " + jsonAuth["username"] + " in progress...")

                ip = jsonAuth["ip"]
                username = jsonAuth["username"]
                publicKey = jsonAuth["publicKey"]

                try:
                    self.clients[ip] = [username]
                    self.clients[ip].append(publicKey)
                    print(username + " authenticated")
                    print(self.clients[ip])
                except Exception as e:
                    print("An error as occured doing the authentication for : " + username)

            except:
                #print("not an auth message")
                #changed
                for connection in self.connections:
                    jsonMsg = json.loads(data)["package"]
                    sender = str(jsonMsg["IP"].replace(" ", ""))
                    connectionIP = str(connection.getpeername()[0])

                    print("connections output")
                    print("-" + sender + "-")
                    print("-" + connectionIP + "-")

                    if(sender != connectionIP):
                        connection.send(bytes(data, 'utf-8'))
                        print(data)
                        if not data:
                            print(str(a[0]) + ':' + str(a[1], 'disconnected'))
                            self.connections.remove(c)
                            c.close()
                            break

    def run(self):
        while self.running:
            c, a = self.sock.accept()

            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()

            self.connections.append(c)
            #self.connections[-1].send(bytes(self.generateJsonClients(), 'utf-8'))
            print(str(a[0]) + ':' + str(a[1]) + ' connected')

        print("Server is now offline")
        exit()

    def generateJsonClients(self):
        #TODO: add the nodes to json
        json = '{'
        json += '"clients": {'
        i = 1
        for connection in self.connections:
            json += '"John": {'
            #json += '"IP": "' + connection[0] + '",'
            print(connection)
            json += '"Public key": "MFswDQYJKoZIhvcNAQEBBQADSgAwRwJAV2"'
            json += '}'
            if i != len(self.connections):
                json += ','
        json += '}'
        json += '}'
        return json

server = Server()
server.run()