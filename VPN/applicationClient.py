from socket import *


def client_program():
    host = '192.168.26.10'  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket(AF_INET, SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = ["request", "wait", "response"]  # take input
    count = 0
    data = 'init'
    for msg in message:
        client_socket.send(msg.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal
 # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
