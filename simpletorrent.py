import socket
import threading

lock = threading.Lock()

class Server:
    def __init__(self, my_port):
        self.port = my_port
        self.sock = None
        self.peers = {}
        self.peers_counter = 0

    def bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("localhost", self.port))
        self.sock.listen(5)
        print("Socket is opened\r\nport : " + str(self.port))
        while True:
            conn, addr = self.sock.accept()
            self.peers[self.peers_count] = (conn, addr)
            self.peers_counter += 1
            print(self.peers[self.peers.count-1] + "is entered")

        self.sock.close()
        print("server is terminated")

if __name__ == '__main__':
    server = Server(30000)
    server.bind()