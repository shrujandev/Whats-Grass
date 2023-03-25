from socket import *
import threading
host = ''  # VPN server
port = 9999

# client_socket = socket(AF_INET, SOCK_STREAM)
# client_socket.connect((host, port))
class ZKAThread(threading.Thread):
    def __init__(self, clientAddr, clientSocket):
        threading.Thread.__init__(self)
        self.cSocket = clientSocket
        self.cAddr = clientAddr
        print("New connection added :", clientAddr)

    def run(self):
        print("\nConnction from ", self.cAddr)
        # while True:
        data = self.cSocket.recv(1024).decode()
        data = "this is from zka"
        # if not data:
        #     break

        self.cSocket.send(data.encode())
        self.cSocket.close()
        print("\nConnction from ", self.cAddr, " closed Successfully")


def vpnZKA():
    host = ''
    port = 9999

    server_socket = socket(AF_INET, SOCK_STREAM)  
    server_socket.bind((host, port))

    while (True):
        server_socket.listen(1)
        cSoc, addr = server_socket.accept()
        newThread = ZKAThread(addr, cSoc)
        newThread.start()

if __name__ == '__main__':
    vpnZKA()