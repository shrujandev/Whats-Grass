from socket import *
import threading
import os
import tqdm

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
            sendFile("ad_list.csv", self.cSocket)
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
    filesize = os.path.getsize(filename)
    socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
    with open(filename, "rb") as f:
        while True:
            bytesRead = f.read(BUFFER_SIZE)
            if not bytesRead:
                break
            socket.sendall(bytesRead)


if __name__ == '__main__':
    vpnZKA()
