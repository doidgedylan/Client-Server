from socket import *
from getpass import getpass
import sys
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
count = 0 
while True:
    correctPassword = "0"
    username = input("Username: ")
    password = getpass("Password: ")
    print()
    clientSocket.send(username.encode())
    clientSocket.send(password.encode())
    correctPassword = clientSocket.recv(1024).decode()
    if correctPassword == "1":
        print("Username and password entered correctly.")
        break
    else:
        print("Username and/or password entered incorrectly.")
while True:
    command = input('Input command (in all capital letters): ')
    if command == "WRITE":
        clientSocket.send(command.encode())
        fileName = input('Enter file name to write: ')
        clientSocket.send(fileName.encode())
        message = input('Write message to the file: ')
        clientSocket.send(message.encode())
    elif command == "READ":
        clientSocket.send(command.encode())
        fileName = input('Enter file name to read: ')
        clientSocket.send(fileName.encode())
        fileFound = clientSocket.recv(1024).decode()
        message = clientSocket.recv(1024).decode()
        if (fileFound == "1"):
            print(message)
        else:
            print('File could not be found')
    elif command == "DELETE":
        clientSocket.send(command.encode())
        fileName = input('Enter file name to delete: ')
        clientSocket.send(fileName.encode())
        fileFound = clientSocket.recv(1024).decode()
        if (fileFound == "1"):
            print('File deleted successfully')
        else:
            print('File not found')
    elif command == "LIST":
        clientSocket.send(command.encode())
        message = clientSocket.recv(1024).decode()
        print('List of files in server: ' + message)
    elif command == "APPEND":
        clientSocket.send(command.encode())
        fileName = input('Enter file name to append: ')
        clientSocket.send(fileName.encode())
        message = input('Write message to append: ')
        clientSocket.send(message.encode())
    elif command == "EXIT":
        clientSocket.send(command.encode())
        clientSocket.close()
        break
    elif ("READ" in command or "WRITE" in command or "DELETE" in command or "APPEND" in command or "LIST" in command or "EXIT" in command):
        print('Invalid command. Type one command in all caps to execute it.')
    else:
        print('Invalid command. Please choose from the following commands: \nWRITE\nREAD\nDELETE\nAPPEND\nLIST\nEXIT')
