from socket import *

def client_program():
    host = '192.168.26.244'  
    port = 5000  

    client_socket = socket(AF_INET, SOCK_STREAM)  
    client_socket.connect((host, port))  
    client_socket.send("ad_response".encode())
    while(True):
        data=client_socket.recv(1024).decode()
        if data.lower().strip()=='ad_request':
            print("Received AD request from server")
            print("Sent AD response to server")

    client_socket.close()  


if __name__ == '__main__':
    client_program()
