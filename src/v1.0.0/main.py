import os
import socket
import threading
import sys
import json
import banner
import time

from cryptogen import PrivateKey, PublicKey

debug = False

class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []

	def __init__(self):
		self.sock.bind(('0.0.0.0', 10000))
		self.sock.listen(1)

	def handler(self, c, a):
		while True:
			data = c.recv(1024)
			for connection in self.connections:
				connection.send(data)
				if not data:
					print(str(a[0]) + ':' + str(a[1], 'disconnected'))
					self.connections.remove(c)
					c.close()
					break

	def run(self):
		while True:
			c, a = self.sock.accept()
			cThread = threading.Thread(target=self.handler, args=(c, a))
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			print(str(a[0]) + ':' + str(a[1]) + ' connected')

class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	__ip = ""
	__username = ""
	__publicKey = PublicKey()
	__privateKey = PrivateKey()

	def __init__(self, address):
		startup = time.time() * 1000
		timeout = time.time() + 60

		while True:
			try:
				self.sock.connect((address, 10000))
				break
			except:
				print("waiting for the server")
				time.sleep(2.5)

			if time.time() > timeout:
				print("No response from " + address)
				exit()

		response_time = int((time.time() * 1000) - startup)
		if response_time != 0:
			if int(response_time / 1000) == 0:
				print("Response time: " + str(response_time) + "ms")
			else:
				print("Response time: " + str(response_time) + "s")
		else:
			print("Response time: 1ms")

		self.__ip = socket.gethostbyname(socket.gethostname())
		self.__username = str(input("What's your username? \n"))

		print("connected as " + self.__username)

		try:
			bytes(self.createAuthJson(), 'utf-8')
		except Exception as e:
			print(e)
		self.sock.send(bytes(self.createAuthJson(), 'utf-8'))

		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True
		iThread.start()

		while True:
			data = self.sock.recv(1024)
			data = data.decode("utf-8")
			if not data:
				if debug == True:
					print("not data")
				break
			try:
				packageJson = json.loads(data)["package"]
				if debug == True:
					print("package:")
					print(packageJson)
				#sys.stdout.write("\033[F")
				print(packageJson["username"] + " : " + packageJson["message"])
			except Exception as e:
				print("ERROR: \n")
				print(e)
			

	def sendMsg(self):
		while True:
			messageTxt = ""
			messageInput = str(input(messageTxt)).replace(messageTxt,"")
			print(self.createPackageJson(messageInput))
			self.sock.send(bytes(self.createPackageJson(messageInput), 'utf-8'))

	def createPackageJson(self, message):
		json =  '{'
		json += '"package": {'
		json += '"IP": "' + self.__ip + '",'
		json += '"username": "' + self.__username + '",'
		json += '"message": "' + message + '"'
		json += '}'
		json += '}'

		if (debug):
			print(json)
		
		return json

	def createAuthJson(self):
		json = '{'
		json += '"auth": {'
		json += '"ip": "' + self.__ip + '",'
		json += '"username": "' + self.__username + '",'
		json += '"publicKey": "' + self.__publicKey.get_key() + '"'
		json += '}'
		json += '}'

		if (debug):
			print(json)
		
		return json

#clear the screen

try:
	os.system('clear')
except:
	os.system('cls')
	
banner.generateBanner("The onion chat")

if (len(sys.argv) > 1):
	time.sleep(3)

	print("Trying to connect to : " + sys.argv[1])
 
	client = Client(sys.argv[1])
else:
	server = Server()
	server.run()
