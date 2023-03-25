from socket import *

host = '' # VPN server  
port = 9999

client_socket = socket(AF_INET, SOCK_STREAM)  
client_socket.connect((host, port)) 

while(True):
    data=client_socket.recv(1024).decode()
    if data.lower().strip()=='ad_request':
        client_socket.send("ad_response".encode())
