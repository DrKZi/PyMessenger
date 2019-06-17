import socket


class MySocket:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect(("127.0.0.1", 8000))

    def get_data(self):
        return self.sock.recv(4096)

    def close(self):
        self.sock.send("DIS".encode())
        self.sock.close()

    def send(self, text):
        self.sock.send(("M1|" + text).encode())
