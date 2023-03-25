from socket import *
import threading


class ServerThread(threading.Thread):
    def __init__(self, clientAddr, clientSocket):
        threading.Thread.__init__(self)
        self.cSocket = clientSocket
        self.cAddr = clientAddr
        print("New connection added :", clientAddr)

    def run(self):
        print("\nConnction from ", self.cAddr)
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = self.cSocket.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            # print("from connected user: " + str(data))

            self.cSocket.send(data.encode())
        self.cSocket.close()
        print("\nConnction from ", self.cAddr, " Closed Successfully")


def server_program():
    # get the hostname
    host = ''
    port = 5000  # initiate port no above 1024

    server_socket = socket(AF_INET, SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously

    while (True):
        server_socket.listen(1)
        cSoc, addr = server_socket.accept()
        newThread = ServerThread(addr, cSoc)
        newThread.start()


if __name__ == '__main__':
    server_program()
