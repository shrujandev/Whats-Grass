from socket import *
import tqdm
import os

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
host = '192.168.26.10'  # as both code is running on same pc
port = 5008  # socket server port number


def client_program():

    client_socket = socket(AF_INET, SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = ["request", "wait", "response"]  # take input

    data = 'init'
    for msg in message:
        client_socket.send(msg.encode())  # send message
        if msg == "request":
            fileMData = client_socket.recv(BUFFER_SIZE).decode()
            filename, filesize = fileMData.split(SEPARATOR)
            recieveFile(client_socket, filename, filesize)
        else:
            data = client_socket.recv(1024).decode()  # receive response
            print('Received from server: ' + data)  # show in terminal
 # again take input

    client_socket.close()  # close the connection


def recieveFile(socket, filename, filesize):
    filename = "thisfromVPN"+str(filename)+".txt"
    filesize = int(filesize)
    print("Matadata Recieved")
    with open(filename, "wb") as f:
        while True:
            try:
                bytesRead = socket.recv(BUFFER_SIZE)
                if not bytesRead:
                    f.close()
                    break
                f.write(bytesRead)
                print("Writing")
            except:
                pass
                break
        f.close()

        print("done")


if __name__ == '__main__':
    client_program()
