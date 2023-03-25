from socket import *
import threading
from time import *
import os

zkaHost = '192.168.26.154'
zkaPort = 9994

host = ''
port = 5008
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

class ServerThread(threading.Thread):
    def __init__(self, clientAddr, clientSocket):
        threading.Thread.__init__(self)
        self.cSocket = clientSocket
        self.cAddr = clientAddr
        print("New connection added :", clientAddr)

    def run(self):
        print("\nConnection from ", self.cAddr)
        while True:
            data = self.cSocket.recv(1024).decode()
            if not data:
                break
            data = parseData(data, self.cSocket, str(
                threading.current_thread().ident))
            # self.cSocket.send(data.encode())
        socketClose(self.cSocket, self.cAddr)

def server_program():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))  
    while True:
        server_socket.listen(1)
        cSoc, addr = server_socket.accept()
        newThread = ServerThread(addr, cSoc)
        newThread.start()

def connectZKA():
    zkaSocket = socket(AF_INET, SOCK_STREAM)
    zkaSocket.connect((zkaHost, zkaPort))
    return zkaSocket


def parseData(data, vpnSocket, threadID):
    if data == "request":
        zSoc = connectZKA()
        zSoc.send(data.encode())
        fileMData = zSoc.recv(BUFFER_SIZE).decode()
        filename, filesize = fileMData.split(SEPARATOR)
        recieveFile(zSoc, filesize, threadID)
        sendFile(vpnSocket, threadID)
        return data
    elif data == "wait":
        sleep(2)
        return "Waited"
    elif data == "response":
        return "This is a response endcomms"
    else:
        return "Invalid"


def recieveFile(socket, filesize, threadID):
    filename = "revievedFromZKA"+threadID+".csv"
    filesize = int(filesize)

    with open(filename, "wb") as f:
        while True:
            try:
                bytesRead = socket.recv(BUFFER_SIZE)
                if not bytesRead:
                    break
                f.write(bytesRead)
            except:
                pass
                break


def sendFile(socket, threadID):
    filename = "revievedFromZKA"+threadID+".csv"
    filesize = os.path.getsize(filename)
    socket.send(f"{threadID}{SEPARATOR}{filesize}".encode())
    with open(filename, "rb") as f:
        while True:
            bytesRead = f.read(BUFFER_SIZE)
            if not bytesRead:
                print("broke")
                break
            socket.sendall(bytesRead)
            # print("\nSending")
        f.close()
        socket.close()
    os.remove(filename)
    return

def socketClose(socket, Addr):
    socket.close()
    print("\nConnction from ", Addr, " Closed Successfully")

if __name__ == '__main__':
    server_program()