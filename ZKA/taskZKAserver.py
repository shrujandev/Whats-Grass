from socket import *
import threading
import os
import tqdm
import csv
import random 

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

host = ''
port = 9994


class ZKAThread(threading.Thread):
    def __init__(self, clientAddr, clientSocket):
        threading.Thread.__init__(self)
        self.cSocket = clientSocket
        self.cAddr = clientAddr
        print("New connection added :", clientAddr)

    def run(self):
        print("\nConnction from ", self.cAddr)
        data = self.cSocket.recv(1024).decode()

        if data == "request":
            with open("ads.csv", "r") as file:
                reader = csv.reader(file)
                num_lines = sum(1 for row in reader)
                file.seek(0)
                line_numbers = random.sample(range(num_lines), 500)
                selected_lines = []
                for i, row in enumerate(reader):
                    if i in line_numbers:
                        # while True:
                        #     if row=='':
                        #         row=next(reader)
                        #         continue
                        selected_lines.append(row)
                        
                            # break
                            # f.write(row+'\n')
            
            f = open("selected_list.csv", "w")
            data=('\n'.join(','.join(x) for x in selected_lines))
            f.write(data)
            f.close()
            sendFile("selected_list.csv", self.cSocket)
            print("Sent AD list to server")
            # self.cSocket.send(';'.join(selected_lines))
        else:
            self.cSocket.send(data.encode())
        self.cSocket.close()
        print("\nConnction from ", self.cAddr, " closed Successfully")

def vpnZKA():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))

    while (True):
        server_socket.listen(1)
        cSoc, addr = server_socket.accept()
        newThread = ZKAThread(addr, cSoc)
        newThread.start()

def sendFile(filename, socket):
    # filesize = os.path.getsize(filename)
    socket.send(f"{filename}{SEPARATOR}{5000}".encode())
    with open(filename, "rb") as f:
        while True:
            bytesRead = f.read(BUFFER_SIZE)
            print(bytesRead)
            if not bytesRead:
                break
            socket.sendall(bytesRead)


if __name__ == '__main__':
    vpnZKA()
