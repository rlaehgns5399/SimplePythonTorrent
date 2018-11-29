import socket
import threading
import argparse

lock = threading.Lock()

parser = argparse.ArgumentParser()
parser.add_argument("-port", help="your port")
arg = parser.parse_args()

class Server(threading.Thread):
    def __init__(self, my_port):
        threading.Thread.__init__(self)
        self.port = my_port
        self.sock = None
        self.peers = {}
        self.peers_counter = 0

    def bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("localhost", self.port))
        self.sock.listen(5)
        print("Socket is opened\r\nport : " + str(self.port))
        self.sendFirstMsg()
        while True:
            conn, addr = self.sock.accept()
            self.peers[self.peers_counter] = (conn, addr)
            self.peers_counter += 1
            print("{} entered".format(addr))

        self.sock.close()
        print("server is terminated")

    def run(self):
        self.bind()

    def sendFirstMsg(self):
        for i in range(self.port+1, self.port+10):
            try:
                temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_socket.connect(("localhost", i))
            except ConnectionRefusedError:
                pass

if __name__ == '__main__':
    server = Server(int(arg.port))
    server.start()