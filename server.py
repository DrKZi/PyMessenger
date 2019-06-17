import sys
import socket
import select
import time

HOST = '127.0.0.1'
SOCKET_LIST = {}
RECV_BUFFER = 4096
PORT = 8000

USERS = {}
ID = 1
all_data = []


def chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    global ID
    SOCKET_LIST['server'] = server_socket

    print("Chat server started on port " + str(PORT))

    try:
        while True:
            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST.values(), [], [], 0)

            for sock in ready_to_read:
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    SOCKET_LIST[str(ID)] = sockfd
                    sockfd.send(("SOCKETID" + str(ID)).encode())
                    ID += 1
                    print("Client {} connected".format(addr))
                else:
                    try:
                        data = sock.recv(RECV_BUFFER).decode()
                        datastr = data.split("|")

                        if datastr[0] == 'USER':
                            for i in USERS:
                                SOCKET_LIST[datastr[1]].send(("USERADD" + i).encode())
                            USERS[datastr[2]] = datastr[1]
                            broadcast("USERADD" + datastr[2])

                        if datastr[0] == 'M1':
                            all_data.append((datastr[1], datastr[2], datastr[3]))
                            if datastr[1] == datastr[2]:
                                send_last(datastr[1], datastr[1], datastr[3])
                            else:
                                send_last(datastr[2], datastr[1], datastr[3])
                                send_last(datastr[1], datastr[1], datastr[3])
                            print(all_data)

                        if datastr[0] == 'M2':
                            SOCKET_LIST[USERS[datastr[1]]].send("RESP".encode())
                            SOCKET_LIST[USERS[datastr[2]]].send("RESP".encode())
                            response(datastr[1], datastr[2])

                        if datastr[0] == 'DIS':
                            if SOCKET_LIST[USERS[datastr[1]]]:
                                del SOCKET_LIST[USERS[datastr[1]]]
                            if USERS[datastr[1]]:
                                del USERS[datastr[1]]
                            broadcast("SYSTEMUser {} leave(died)!".format(datastr[1]))
                            cleaning(datastr[1])
                            print("Client {} disconnected".format(addr))
                            print(all_data)

                    except ConnectionResetError:
                        broadcast("SYSTEMUser leave(died) with error!")
                        print("Client {} disconnected with exception!".format(addr))
                        continue

    except KeyboardInterrupt:
        server_socket.close()
        all_data.clear()
        print("Server closing...")


def response(you, user):
    for mess in all_data:
        if (mess[0] == you and mess[1] == user) or (mess[0] == user and mess[1] == you):
            send_last(mess[0], mess[0], mess[2])
            send_last(mess[1], mess[0], mess[2])


def cleaning(name):
    global all_data
    deleting_data = [i for i in all_data if i[0] == name]
    temp = [x for x in all_data if x not in deleting_data]
    all_data.clear()
    all_data = temp


def send_last(user, name, mess):
    try:
        SOCKET_LIST[USERS[user]].send(name.encode())
        time.sleep(0.01)
        SOCKET_LIST[USERS[user]].send(mess.encode())
    except OSError:
        SOCKET_LIST[USERS[user]].close()
        if socket in SOCKET_LIST:
            del SOCKET_LIST[USERS[user]]


def broadcast(message):
    for_del = []
    for socket in SOCKET_LIST:
        if not socket == 'server':
            try:
                SOCKET_LIST[socket].send(message.encode())
            except OSError:
                print("OSERROR")
                SOCKET_LIST[socket].close()
                for_del.append(socket)
    for i in for_del:
        del SOCKET_LIST[i]



if __name__ == "__main__":
    sys.exit(chat_server())
