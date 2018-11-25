import socket
import threading
import argparse

ENCODING = 'utf-8'

parser = argparse.ArgumentParser()
parser.add_argument("--port", help='your Port')
parser.add_argument("--dport", help="your friend's Port")
parser.add_argument("--file", help='.simpletorrent file')
args = parser.parse_args()

ip = '192.168.0.18'

class Receiver(threading.Thread):
    def __init__(self, my_host, my_port):
        threading.Thread.__init__(self, name="client_receiver")
        self.host = my_host
        self.port = my_port

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(10)
        while True:
            connection, client_address = sock.accept()
            try:
                full_message = ""
                while True:
                    data = connection.recv(16)
                    full_message = full_message + data.decode(ENCODING)
                    if not data:
                        print("{}: {}".format(client_address, full_message.strip()))
                        break
            finally:
                connection.shutdown(2)
                connection.close()
    def run(self):
        self.listen()

class Sender(threading.Thread):
    def __init__(self, my_friends_host, my_friends_port):
        threading.Thread.__init__(self, name="client_sender")
        self.host = my_friends_host
        self.port = my_friends_port

    def run(self):
        while True:
            message = input("")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.sendall((message.encode(ENCODING)))
            s.shutdown(2)
            s.close()

def main():
    my_host = "localhost"
    my_port = int(args.port)
    receiver = Receiver(my_host, my_port)
    my_friends_host = "localhost"
    my_friends_port = int(args.dport)
    sender = Sender(my_friends_host, my_friends_port)
    treads = [receiver.start(), sender.start()]

if __name__ == '__main__':
    main()
