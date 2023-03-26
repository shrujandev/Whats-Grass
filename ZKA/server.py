from socket import *
import threading
import os 

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
class ServerThread(threading.Thread):
    def __init__(self, clientAddr, clientSocket):
        threading.Thread.__init__(self)
        self.cSocket = clientSocket
        self.cAddr = clientAddr
        print("New connection added :", clientAddr)

    def run(self):
        print("\nConnection from ", self.cAddr)
        while True:
            data = self.cSocket.recv(4096).decode()
            if not data:
                break
            f=open("ads_list.csv","a", encoding='utf-8')
            f.write(data)
            f.close()
        self.cSocket.close()
        print("\nConnection from ", self.cAddr, " closed Successfully")

def sendFile(filename, socket):
    filesize = os.path.getsize(filename)
    socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
    with open(filename, "rb") as f:
        while True:
            bytesRead = f.read(BUFFER_SIZE)
            if not bytesRead:
                break
            socket.sendall(bytesRead)


client_list=[]
host = ''
port = 5000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((host, port))
print("Server started...")
while (True):
    server_socket.listen(1)
    cSoc, addr = server_socket.accept()
    client_list.append(cSoc)
    newThread = ServerThread(addr, cSoc)
    newThread.start()
    # if len(client_list)==2:
    #     print("All clients connected")
    #     break

ad_list=[]
while(True):
    message = input("")
    if message.lower().strip() == 'ad_request':
        for c in client_list:
            c.send(message.encode())
            data = c.recv(1024).decode()
            ad_list.append(data)

