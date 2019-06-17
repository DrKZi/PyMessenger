import sys
import socket
import select

HOST = '127.0.0.1'
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 8000


def chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    SOCKET_LIST.append(server_socket)

    print("Chat server started on port " + str(PORT))

    while True:
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("Client {} connected".format(addr))
                # broadcast(server_socket, "{} entered our chatting room\n".format(addr))
            else:
                try:
                    data = sock.recv(RECV_BUFFER).decode()
                    datastr = data.split("|")
                    if datastr[0] == 'M1':
                        broadcast(server_socket, datastr[1])
                        broadcast(server_socket, datastr[2])
                    if datastr[0] == 'DIS':
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        broadcast(server_socket, "SYSTEM")
                        broadcast(server_socket, "User [some user] leave(died)!")
                        print("Client {} disconnected".format(addr))
                except ConnectionResetError:
                    broadcast(server_socket, "SYSTEM")
                    broadcast(server_socket, "User [some user] leave(died)!")
                    print("Client {} disconnected".format(addr))
                    continue

    server_socket.close()


def broadcast(server_socket, message):
    for socket in SOCKET_LIST:
        if socket != server_socket:
            try:
                socket.send(message.encode())
            except OSError:
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


if __name__ == "__main__":
    sys.exit(chat_server())
