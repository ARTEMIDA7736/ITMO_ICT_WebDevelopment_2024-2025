import socket
import threading
from dataclasses import dataclass
from enum import Enum

class UserState(Enum):
    NONE = -1
    CONNECTED = 0
    READY = 1

@dataclass
class User:
    conn: socket.socket
    state: UserState = UserState.NONE
    name: str = ""

class Server:
    def __init__(self, ip, port):
        self.running = True
        self.users: list[User] = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen()
        print("Server is listening")

        self.receive()

    def stop(self):
        self.running = False
        self.sock.close()
        print("Server stopped")

    def broadcast(self, label: str, message: str, except_list: list[User] = None):
        if except_list is None:
            except_list = []

        full_message = f"{label}: {message}"
        print(full_message)

        for user in self.users:
            if user.state != UserState.READY or user in except_list:
                continue
            user.conn.sendall(full_message.encode(encoding))

    def send_message(self, user: User, message: str):
        user.conn.sendall(message.encode(encoding))

    def process_user(self, conn: socket.socket):
        user = User(conn=conn, state=UserState.CONNECTED, name="")
        self.users.append(user)
        while self.running:
            try:
                if user.state == UserState.NONE:
                    user.state = UserState.CONNECTED
                elif user.state == UserState.CONNECTED:
                    self.send_message(user, "What is your name?")
                    name = conn.recv(buffer_size).decode(encoding)
                    if not name:
                        raise ValueError()

                    user.name = name
                    user.state = UserState.READY
                    self.broadcast(user.name, "connected")
                elif user.state == UserState.READY:
                    message = conn.recv(buffer_size).decode(encoding)
                    self.broadcast(user.name, message, [user])
            except:
                conn.close()
                self.users.remove(user)
                self.broadcast(user.name, "disconnected")
                break

    def receive(self):
        while self.running:
            conn, addr = self.sock.accept()
            print("Incoming connection", addr)

            thread = threading.Thread(target=self.process_user, args=(conn,))
            thread.start()

if __name__ == "__main__":
    encoding = "utf-8"
    buffer_size = 1024
    server_addr = "localhost"
    server_port = 8080
    Server(server_addr, server_port)
