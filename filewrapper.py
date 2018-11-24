import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--file", help='to wrap file')
args = parser.parse_args()


file_size = os.path.getsize(args.file)

with open(args.file, "rb") as f:
    byte = f.read(1)