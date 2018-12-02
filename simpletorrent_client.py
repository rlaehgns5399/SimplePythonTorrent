import socket
import argparse
import threading
import json
import random
import pickle

from random import shuffle

parser = argparse.ArgumentParser()
parser.add_argument("-port", help="to connect server, enter port")
args = parser.parse_args()

target_file = None
my_file_list = []

def openfile(sock, data):
    global my_file_list
    my_file_list = []

    tempshufflelist = []
    with open(data, "r") as f:
        target_file = json.load(f)
        # pick 0 ~ 10
        howmany = random.randrange(8, 10)
        for i in range(0, 10):
            tempshufflelist.append(i)
        shuffle(tempshufflelist)
        tempshufflelist = tempshufflelist[0:howmany]
        for i in tempshufflelist:
            my_file_list.append(target_file["hash_list"][i])
        target_file["hash_list"] = my_file_list
        print("result: there are " + str(howmany*100/10) + "% of file")
        print(my_file_list)

        sock.sendall(pickle.dumps(target_file))


def recvmsg(sock):
    global target_file

    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            data = data.decode("utf-8")
            if data == "go_ahead":
                print("[*] received upload request. input simpletorrent file")
            elif data == "go_ahead_another":
                print("[*] Server doesn't allow to input something. wait")
            else:
                print("[*] find " + data)

                findThread = threading.Thread(target=openfile, args=(sock, data,))
                findThread.daemon = True
                findThread.start()

        except:
            pass

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", int(args.port)))
print("[*] connected to server:", int(args.port))

recvThread = threading.Thread(target=recvmsg, args=(server,))
recvThread.daemon = True
recvThread.start()

while True:
    msg = input("")
    if msg == "exit":
        server.sendall("bye".encode("utf-8"))
        break
    server.sendall(msg.encode("utf-8"))