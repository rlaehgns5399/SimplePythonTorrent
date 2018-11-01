import socket
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", help='Port')
parser.add_argument("--file", help='.simpletorrent file')
args = parser.parse_args()

ip = '192.168.0.18'

if __name__ == '__main__':
    print("Port", args.port)
    print("TorrentFileName:", args.file)
    # (args.port)