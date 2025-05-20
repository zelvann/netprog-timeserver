import socket
import threading
from datetime import datetime

endline = "\r\n"
char_encode = "utf-8"


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        buffer = ""
        while True:
            data = self.connection.recv(32)
            if not data:
                break
            buffer += data.decode(char_encode)

            # buffer harus berisi karakter 13 dan 10
            while endline in buffer:
                line, buffer = buffer.split(endline, 1)
                if line == "TIME":
                    now = datetime.now().strftime("%H:%M:%S")
                    resp = f"JAM {now}{endline}"
                    self.connection.sendall(resp.encode(char_encode))
                elif line == "QUIT":
                    print(f"{self.address} sent QUIT. Closing connection")
                    self.connection.close()
                    return
                else:
                    self.connection.sendall(
                        f"Invalid command{endline}".encode(char_encode)
                    )
        self.connection.close()


class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.my_socket.bind(("0.0.0.0", 45000))
            self.my_socket.listen(1)
            while True:
                self.connection, self.client_address = self.my_socket.accept()
                print(f"connection from {self.client_address}")

                clt = ProcessTheClient(self.connection, self.client_address)
                clt.start()
                self.the_clients.append(clt)
        finally:
            self.my_socket.close()


def main():
    svr = Server()
    svr.start()


if __name__ == "__main__":
    main()
