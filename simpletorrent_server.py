import socket
import threading
import argparse
import time
import json
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("-port", help="your server port")
arg = parser.parse_args()

status = None
peer_count = 0
target_file = None
peer_data_list = []

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
    global conn_array
    global status
    global target_file
    global peer_data_list
    global peer_count

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
        try:
            data = conn.recv(8092)
            if status != 1:
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
                peer_count = 0
                peer_data_list = []
                sem.release()

                print("[*] Server received file name: " + data)
                print("[*] Find peers who has file")

                broadcast_except_requester(data, conn)

            elif status == 1 and data is not None:

                sem.acquire()
                peer_count += 1
                temp_item = pickle.loads(data)
                peer_data_list.append(temp_item)
                print("{} >> ".format(port), json.dumps(temp_item))
                if peer_count == len(conn_array)-1:
                    status = 2
                    print("[*] Collecing data.... Done")
                sem.release()
        except ConnectionResetError:
            print("[*] port " + str(port) + " - bye~!")
            break
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