import socket
import os
import sys
import select

SERVER_IP = '10.12.26.110'
SERVER_PORT = 3001
RECV_BUFR = 4096
USERS_CONNECT = []
SOCKET = []
USERNAME = []
LINE = "\n##################################################################\n"

def chat_client():
    """
    Runs a chat client that connects to a given server. The user can receive and
    send messages to the server.
    """
    # ask for USERNAME
    USERNAME.append(input("USERNAME > "))

    # attempt to connect
    if connect_to_server(USERNAME[0]) == 1:
        print(LINE+" Connected to "+SERVER_IP+LINE)
        prompt()

        while 1:
            try:
                socket_list = [sys.stdin, SOCKET[0]]

                # Get the list sockets which are readable
                read_sockets, write_sockets, error_sockets = \
                select.select(socket_list , [], [],)

                for sock in read_sockets:
                    # incoming message from remote server
                    if sock == SOCKET[0]:
                        recv_msg(sock)

                    # user entered a message
                    else:
                        send_msg(SOCKET[0],sys.stdin.readline())
            except:
                print("ERROR: Lost connection.")
                sys.exit()


def prompt():
    """
    Prints out the chat prompt.
    """
    sys.stdout.write(USERNAME[0]+" > ")
    sys.stdout.flush()


def send_msg(server_socket,msg):
    """
    Allows a user to send a message to the chat server using the given socket.
    """
    server_socket.send(bytes(msg,'UTF-8'))
    prompt()


def recv_msg(socket):
    """
    Allows the program to recieve a message on the given socket.
    """
    data = socket.recv(bytes(RECV_BUFR,'UTF-8'))
    if not data :
        print("Disconnected from the chat server")
        sys.exit()
    else:
        # print data
        sys.stdout.write(data)
        prompt()


def connect_to_server(username):
    """
    Attempts to connect to the server using the given username.
    """
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((SERVER_IP, SERVER_PORT))
        clientsocket.send(bytes(username,'UTF-8'))
        clientsocket.settimeout(30)
        ack = clientsocket.recv(RECV_BUFR).decode()

        if ack != "NOT_UNIQUE":
            SOCKET.append(clientsocket)
            return 1
        else:
            return 0
    # chat server offline
    except(ConnectionRefusedError):
        print("Server offline")
        return -1


if __name__ == "__main__":
    chat_client()