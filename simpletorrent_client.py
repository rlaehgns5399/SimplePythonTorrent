import socket
import argparse
import threading

parser = argparse.ArgumentParser()
parser.add_argument("-port", help="to connect server, enter port")
args = parser.parse_args()

allowInput = True

def recvmsg(sock):
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

        except:
            pass

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", int(args.port)))
print("[*] connected to server:", int(args.port))

recvThread = threading.Thread(target=recvmsg, args=(server,))
recvThread.daemon = True
recvThread.start()

while allowInput:
    msg = input("")
    if msg == "exit":
        server.sendall("bye".encode("utf-8"))
        break
    server.sendall(msg.encode("utf-8"))