from socket import *
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

def sendFile(filename, socket):
    filesize = os.path.getsize(filename)
    socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
    with open(filename, "rb") as f:
        while True:
            bytesRead = f.read(BUFFER_SIZE)
            if not bytesRead:
                break
            socket.sendall(bytesRead)

def client_program():
    host = '192.168.26.244'
    port = 5000
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))
    # client_socket.send("ad_response".encode())
    sendFile("ZKA/urls1.csv", client_socket)
    print("Sent AD list to server")
    # while(True):
    #     data=client_socket.recv(1024).decode()
    #     if data.lower().strip()=='ad_request':
    #         print("Received AD request from server")
    client_socket.close()

if __name__ == '__main__':
    client_program()