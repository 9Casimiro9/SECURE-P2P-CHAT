class Node:
    def outputClients(self, clients):
        print(("-" * 10) + "CLIENTS OUTPUT" + ("-" * 10))

        if len(clients) == 0:
            print("NO CLIENTS ONLINE!")

        for c in clients:
            print('client : ' + c.getUsername() + ' ¦ ip : ' + c.getIp())

    def outputConnections(self, connections, clients):
        #TODO create connections dict and pass hte authconnection to True
        print(("-" * 10) + "CONNECTIONS OUTPUT" + ("-" * 10))

        if len(connections) == 0:
            print("NO CONNECTIONS!")

        for connection in connections:
            authConnection = False
            for client in clients:
                if connection.getpeername()[0] == client.getIp():
                    authConnection = True
                    break

            print('connection : ' + connection.getpeername()[0] + ' ¦ auth : ' + str(authConnection))

    def outputClientsKeys(self,clients):
        print(("-" * 10) + "CLIENTS OUTPUT" + ("-" * 10))

        if len(clients) == 0:
            print("NO CLIENTS ONLINE!")

        for c in clients:
            print('client : ' + c.getUsername() + ' ¦ ip : ' + c.getIp())
            print(c.getPublicKey())