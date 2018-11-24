import argparse
import os
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument("--file", help='to wrap file')
args = parser.parse_args()


file_size = os.path.getsize(args.file)
# 100 바이트 이하면 가치없다고 판단하고 종료
if file_size < 100:
    print("파일이 너무 작아서 가치가 없습니다.")
    exit()

one_file_size = int(file_size / 10)

file_size_list = [
    one_file_size,
    one_file_size,
    one_file_size,
    one_file_size,
    one_file_size,
    one_file_size,
    one_file_size,
    one_file_size,
    one_file_size,
    file_size - one_file_size * 9
]

print(file_size_list)

def getHash(byte_seq):
    hasher = hashlib.md5()
    hasher.update(byte_seq)
    return hasher.hexdigest()

file_size_index = 0
with open(args.file, "rb") as f:
    for i in range(0, 10):
        byte = f.read(file_size_list[i])
        print(getHash(byte))
