import socket
import threading
import argparse
import time
import json

parser = argparse.ArgumentParser()
parser.add_argument("-port", help="your server port")
arg = parser.parse_args()

status = None
target_file = None
target_file_json = None

conn_array = []
addr_array = []
thread_array = []

sem = threading.Lock()


class Server(threading.Thread):
    def __init__(self, my_port):
        threading.Thread.__init__(self)
        self.port = my_port
        self.sock = None

    def bind(self):
        global conn_array
        global addr_array
        global thread_array

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("localhost", self.port))
        print("port: " + str(self.port))
        self.sock.listen(1)
        while True:
            conn, addr = self.sock.accept()
            conn_array.append(conn)
            addr_array.append(addr)

            client_thread = threading.Thread(target=client, args=(conn, addr[1]))
            client_thread.start()
            thread_array.append(client_thread)


        self.sock.close()
        print("server is terminated")

    def run(self):
        self.bind()


def client(conn, port):
    global status
    global target_file
    # status #
    # 0 : ready
    # 1 : find peers
    #
    # command #
    # c: connect server
    # r: request file
    # filename.simpletorrent after r : server notify file and request to server to find file
    #
    ###
    while True:
        data = conn.recv(1024)
        data = data.decode("utf-8")
        if not data:
            break
        if data == "c":
            print("[*] port {}, Connected to server!".format(port))

        elif data == "r":

            sem.acquire()
            status = 0
            sem.release()

            print("[*] client {} want to request file".format(port))
            conn.sendall("go_ahead".encode("utf-8"))
            broadcast_except_requester("go_ahead_another", conn)

        elif status == 0 and ".simpletorrent" in data:

            sem.acquire()
            status = 1
            target_file = data
            sem.release()

            print("[*] Server received file name: " + data)
            print("[*] Find peers who has file")

            broadcast_except_requester(data, conn)



    conn.close()

def broadcast(text):
    global conn_array

    for conn in conn_array:
        conn.sendall(text.encode("utf-8"))

def broadcast_except_requester(text, conn):
    global conn_array

    for conn_iterator in conn_array:
        if conn_iterator != conn:
            conn_iterator.sendall(text.encode("utf-8"))

# def reply(text):

if __name__ == '__main__':
    server = Server(int(arg.port))
    server.start()