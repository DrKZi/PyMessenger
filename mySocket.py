import socket


class MySocket:
    def __init__(self):
        self.sock = socket.socket()
        try:
            self.sock.connect(("127.0.0.1", 8000))
            self.id = self.sock.recv(4096).decode()[8:]
            self.con = True
        except ConnectionRefusedError:
            self.con = False
            print("Cannot connect to server!")
        self.name = ""

    def get_data(self):
        return self.sock.recv(4096)

    def set_name(self, name):
        self.name = name
        self.sock.send(("USER|" + self.id + "|" + self.name).encode())

    def close(self):
        self.sock.send(("DIS|" + self.name).encode())
        self.sock.close()

    def send(self, to, text):
        self.sock.send(("M1|" + self.name + "|" + to + "|" + text).encode())

    def select_user(self, user):
        self.sock.send(("M2|" + self.name + "|" + user).encode())
