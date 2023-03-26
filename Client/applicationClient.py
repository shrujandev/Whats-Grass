from socket import *
import tqdm
import os
import contentbased as cb
import pandas as pd


BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
host = '192.168.26.10'  # as both code is running on same pc
port = 5026  # socket server port number
REQUEST = "request"


def clientProgram():

    # connect to the server
 # take input

    while True:
        choice = input(
            "\nEnter your Choice \n1.Get Recommendation\n2.Exit\nChoice : ")
        fetchFlag = 0
        request = 0
        if choice == "1":
            selectedDict = dict()
            movie = input("Enter Movie name : ")
            l1 = cb.get_recommendations(movie, cb.cosine_sim2)
            print(l1)
            while fetchFlag == 0:
                client_socket = socket(AF_INET, SOCK_STREAM)  # instantiate
                client_socket.connect((host, port))
                client_socket.send(f"{REQUEST}{SEPARATOR}{request}".encode())
                fileMData = client_socket.recv(BUFFER_SIZE).decode()
                filename, filesize = fileMData.split(SEPARATOR)
                fileDict = recieveFile(client_socket, filename, filesize)
                print(fileDict)
                for i in l1:
                    if i in fileDict.keys():
                        selectedDict[i] = fileDict[i]
                        print("Matched movie : ", i)
                    if len(selectedDict.keys()) >= 3:
                        fetchFlag = 1
                        break
                request = request+1
                client_socket.close()
            print(selectedDict)
        else:
            print("Errror")
            break


def recieveFile(socket, filename, filesize):
    filename = "DataRecv/thisfromTASK"+str(filename)+".csv"
    dictT = dict()
    #filesize = int(filesize)
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
    if os.path.getsize(filename) == 0:
        os.remove(filename)
        return dictT
    print("done")
    return convertDict(filename)


def convertDict(filename):
    dictionary = dict()
    new_df = pd.read_csv(filename, header=None, encoding='utf-8')
    tt = new_df.iloc[:, 2].to_list()
    urls = new_df.iloc[:, 1].to_list()
    dict1 = {}
    for i in range(len(tt)):
        if i == 0:
            continue
        dict1[tt[i]] = urls[i]
    print(dict1)
    os.remove(filename)
    return dict1


if __name__ == '__main__':
    clientProgram()
