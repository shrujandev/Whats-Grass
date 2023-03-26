from socket import *
import threading
from time import *
import os
import logging
logging.basicConfig(filename=".\logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

zkaHost = '192.168.26.244'
zkaPort = 9994

host = ''
port = 5026
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


class ServerThread(threading.Thread):
    def __init__(self, clientAddr, clientSocket):
        threading.Thread.__init__(self)
        self.cSocket = clientSocket
        self.cAddr = clientAddr
        print("New connection added :", clientAddr)
        logger.info("New Connection Added: ",clientAddr)

    def run(self):
        print("\nConnection from ", self.cAddr)
        logger.info(f"Connection from: {self.cAddr} with task Server")

        logger.info("Task Server Running")
        while True:
            data = self.cSocket.recv(1024).decode(encoding="utf-8")
            if not data:
                break
            data = parseData(data, self.cSocket, str(
                threading.current_thread().ident))
            # self.cSocket.send(data.encode())
        socketClose(self.cSocket, self.cAddr)
        logger.info("Task Server Connection closed")


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
    logger.info("Connection established to ZKA server")
    return zkaSocket


def parseData(data, vpnSocket, threadID):
    req, count = data.split(SEPARATOR)
    if req == "request":
        zSoc = connectZKA()
        zSoc.send(req.encode())
        fileMData = zSoc.recv(BUFFER_SIZE).decode(encoding="utf-8")
        filename, filesize = fileMData.split(SEPARATOR)
        recieveFile(zSoc, filesize, threadID)
        logger.info("File Received by Task Server.")
        sendFile(vpnSocket, threadID)
        logger.info("File Sent by Task Server.")
        return req
    elif data == "wait":
        sleep(2)
        return "Waited"
    elif data == "response":
        return "This is a response endcomms"
    else:
        logger.error("Server received an invalid input.")
        return "Invalid"


def recieveFile(socket, filesize, threadID):
    filename = "revievedFromZKA"+threadID+".csv"
    #filesize = int(filesize)
    logger.info(f"Task Server receiving Information on Thread: {threadID}.")
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
        f.close()


def sendFile(socket, threadID):
    filename = "revievedFromZKA"+threadID+".csv"
    filesize = os.path.getsize(filename)
    logger.info(f"Task Server Sending Information on Thread: {threadID}.")
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
    # os.remove(filename)
    return


def socketClose(socket, Addr):
    socket.close()
    print("\nConnection from ", Addr, " Closed Successfully")
    logger.info(f"Connection from {Addr} has been closed.")


if __name__ == '__main__':
    server_program()
