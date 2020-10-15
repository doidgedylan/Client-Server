from socket import*
from hashlib import md5
from getpass import getpass
import sys
import os
check_username = "14c4b06b824ec593239362517f538b29"
check_password = "5f4dcc3b5aa765d61d8327deb882cf99"
fileSet = set()
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive. Listening on port ' + str(serverPort))
connectionSocket, addr = serverSocket.accept()
while True:
    correctPassword = "0"
    username = connectionSocket.recv(1024).decode()
    password = connectionSocket.recv(1024).decode()
    if md5(username.encode()).hexdigest() == check_username:
        if md5(password.encode()).hexdigest() == check_password:
            print("Username and password entered correctly.")
            correctPassword = "1"
            connectionSocket.send(correctPassword.encode())
            break
        else:
            print("Password entered incorrectly.")
    else:
        print("Username entered incorrectly.")
    connectionSocket.send(correctPassword.encode())
while True:
    message = connectionSocket.recv(1024).decode()
    if message == "WRITE":
        print('WRITE received')
        fileName = connectionSocket.recv(1024).decode()
        print('File name received: ' + fileName)
        message = connectionSocket.recv(1024).decode()
        print('Message received: ' + message)
        f = open(fileName, "w+")
        f.write(message)
        f.close()
        fileSet.add(f)
    elif message == "READ":
        print('READ received')
        fileName = connectionSocket.recv(1024).decode()
        print('File name received: ' + fileName)
        fileFound = "0"
        for x in fileSet:
            if (x.name == fileName):
                fileFound = "1"
                f = open(fileName, "r")
                if f.mode == "r":
                    message = f.read()
                    connectionSocket.send(fileFound.encode())
                    connectionSocket.send(message.encode())
        if (fileFound == "0"):
            connectionSocket.send(fileFound.encode())
            message = ""
            connectionSocket.send(fileFound.encode())
    elif message == "DELETE":
        print('DELETE received')
        fileName = connectionSocket.recv(1024).decode()
        print('File name received: ' + fileName)
        fileFound = "0"
        fileSet2 = fileSet
        for x in fileSet:
            if (x.name == fileName):
                os.remove(fileName)
                fileSet2 = fileSet.discard(fileName)
                fileFound = "1"
                connectionSocket.send(fileFound.encode())
                print('File ' + fileName + ' deleted successfully')
        if (fileFound == "0"):
            connectionSocket.send(fileFound.encode())
            print('File not found')
        fileSet = fileSet2
    elif message == "LIST":
        print('LIST received')
        fileList = ""
        for x in fileSet:
            fileList = fileList + '\n' + x.name
        connectionSocket.send(fileList.encode())
    elif message == "APPEND":
        print('APPEND received')
        fileName = connectionSocket.recv(1024).decode()
        print('File name received: ' + fileName)
        message = connectionSocket.recv(1024).decode()
        print('Message received: ' + message)
        f = open(fileName, "a+")
        f.write('\n' + message)
        f.close()
    elif message == "EXIT":
        print('EXIT received')
        connectionSocket.close()
        break
