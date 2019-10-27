import warnings
warnings.simplefilter("ignore", category=DeprecationWarning)

import os
import socket
import threading
import sys
import json
import banner
import time

from cryptogen import PrivateKey, PublicKey
from client import Client
from classes import ProgressBar,JsonWEncryption

debug = False

class Main:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	__ip = ""
	__username = ""
	__publicKey = None
	__privateKey = None
	__clients = []

	def __init__(self, address):
		startup = time.time() * 1000
		timeout = time.time() + 60

		while True:
			try:
				self.sock.connect((address, 10000))
				break
			except:
				print("waiting for " + address)
				time.sleep(2.5)

			if time.time() > timeout:
				print("No response from " + address)
				exit()

		response_time = int((time.time() * 1000) - startup)
		if response_time != 0:
			if int(response_time / 1000) == 0:
				print("Response time: " + str(response_time) + "ms")
			else:
				print("Response time: " + (str(response_time) / 1000 ) + "s")
		else:
			print("Response time: 1ms")

		self.__ip = socket.gethostbyname(socket.gethostname())
		while True:
			self.__username = str(input("What's your username? \n"))

			if self.__username.strip() == "":
				sys.stdout.write("\033[F")
				print("Invalid username")
				print("-!-" * 20)
			else:
				break		

		try:
			self.__privateKey = PrivateKey(debug, self.__username)
			self.__publicKey = PublicKey(debug, self.__username)
		finally:
			print("connected to " + address + " as " + self.__username)

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
			if debug:
				print("data value is :")
				print(data)
			if not data:
				print("Server is now offline")
				if debug:
					print("not data")
				break
			try:
				packageJson = json.loads(data)["package"]
				if debug:
					print("package:")
					print(packageJson)
				#sys.stdout.write("\033[F")
			except Exception as e:
				if debug:
					print("ERROR:")
					print(e)
				
				jwe = JsonWEncryption(debug, data)
				if jwe.label == "package":
					if debug:
						print("package")
					for client in self.__clients:
						if debug:
							print(client.getIp() + "==" + jwe.sender)
						if client.getIp() == jwe.sender:
							print(client.getUsername() + " : " + self.__privateKey.decrypt(jwe.message.encode('ISO-8859-1')))
					continue
				if debug:
					print(data)
					print("json")

				try:
					if debug:
						print(data)
					clientsJson = json.loads(data)["clients"]
					if debug:
						print("clients:")
						print(clientsJson)
					#sys.stdout.write("\033[F")
					self.__clients.clear()
					for clientJson in clientsJson:
						if debug:
							print("client")
							print(clientJson["IP"] + " : " + clientJson["Username"] + " : " + clientJson["PublicKey"])
						client = Client(clientJson["IP"],  clientJson["Username"], clientJson["PublicKey"])
						self.__clients.append(client)
					
					if debug:
						print(self.__clients)

					#print(packageJson["IP"]["username"] + " : " + packageJson["message"])
				except Exception as e:
					print("ERROR:")
					print(e)
				

	def sendMsg(self):
		while True:
			messageTxt = ""
			messageInput = str(input(messageTxt)).replace(messageTxt,"")
			for client in self.__clients:
				try:
					self.sock.send(bytes(self.createPackageJson(messageInput, client), "utf-8"))
					if debug:
						print(self.createPackageJson(messageInput, client))
						print("successfully sent the message to " + client.getIp())
				except Exception as e:
					if debug:
						print("An error as occurred sending the message to : " + client.getIp())
						print(e)

	def createPackageJson(self, message, client):
		jsonData = ""
		try:
			if debug:
				print("createPackageJson")
				print(self.__publicKey.format(client.getPublicKey()))
				print(message)
				print(self.__publicKey.encrypt(message, client.getPublicKey()))
			jsonData =  '{'
			jsonData += '"package": {'
			jsonData += '"IP": "' + self.__ip + '",'
			jsonData += '"username": "' + self.__username + '",'
			jsonData += '"message": "'
			jsonData += self.__publicKey.encrypt(message, self.__publicKey.format(client.getPublicKey())).decode('unicode-escape')
			jsonData += '",'
			jsonData += '"target": "' + client.getIp() + '"'
			jsonData += '}'
			jsonData += '}'
		except Exception as e:
			print("error in createPackageJson")
			print(e)

		if debug:
			print(jsonData)
		
		return jsonData

	def createAuthJson(self):
		jsonData = '{'
		jsonData += '"auth": {'
		jsonData += '"ip": "' + self.__ip + '",'
		jsonData += '"username": "' + self.__username + '",'
		jsonData += '"publicKey": "' + str(self.__publicKey.get_key()) + '"'
		jsonData += '}'
		jsonData += '}'

		if (debug):
			print(jsonData)
		
		return jsonData

#clear the screen

try:
	os.system('clear')
except:
	os.system('cls')
	
banner.generateBanner("The onion chat")

if (len(sys.argv) > 1):
	time.sleep(3)

	print("Trying to connect to : " + sys.argv[1])
 
	Main(sys.argv[1])
else:
	server = Server()
	server.run()
