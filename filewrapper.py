import argparse
import os
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument("--file", help='to wrap file')
args = parser.parse_args()

create_folder = "file/"
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

def getHashName(byte_seq):
    hasher = hashlib.md5()
    hasher.update(byte_seq)
    return hasher.hexdigest()

def checkHash(path, blocksize):
    hash = hashlib.md5()
    with open(create_folder + path, 'rb') as file:
        buf = file.read(blocksize)
        hash.update(buf)
    file.close()
    return hash.hexdigest()

file_size_index = 0
with open(args.file, "rb") as f:
    for i in range(0, 10):
        byte = f.read(file_size_list[i])
        file_name = getHashName(byte)
        with open(create_folder + file_name, "wb") as output:
            output.write(byte)
            output.close()
        print(file_name + " " + str(file_size_list[i]) + " " + checkHash(file_name, file_size_list[i]))