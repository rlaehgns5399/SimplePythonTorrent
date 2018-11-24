import argparse
import os
import hashlib
import json

parser = argparse.ArgumentParser()
parser.add_argument("--file", help='to wrap file')
args = parser.parse_args()

create_folder = "file/"
file_size = os.path.getsize(args.file)
# 100 바이트 이하면 가치없다고 판단하고 종료
if file_size < 100:
    print("파일이 너무 작아서 가치가 없습니다.")
    exit()

# 파일을 10분할로 하되, 마지막 chunk는 그 나머지를 취하도록 구성
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

# byte sequence가 주어지면, md5 값 계산
def getHashName(byte_seq):
    hasher = hashlib.md5()
    hasher.update(byte_seq)
    return hasher.hexdigest()

# 해당 파일의 md5 계산
def checkHash(path, blocksize):
    hash = hashlib.md5()
    with open(create_folder + path, 'rb') as file:
        buf = file.read(blocksize)
        hash.update(buf)
    file.close()
    return hash.hexdigest()

# simpletorrent 파일 형식(json)
json_result = {
    "actual_name": "",
    "hash_list": "",
    "size": ""
}

# hash_list는 md5 해쉬값이 들어간다.
list = []

# 해당 파일을 읽고 md5 파일 이름으로 file 폴더에 저장
with open(args.file, "rb") as f:
    for i in range(0, 10):
        byte = f.read(file_size_list[i])
        file_name = getHashName(byte)
        list.append(file_name)
        with open(create_folder + file_name, "wb") as output:
            output.write(byte)
            output.close()
        # print(file_name + " " + str(file_size_list[i]) + " " + checkHash(file_name, file_size_list[i]))

# simpletorrent file 포맷에 집어 넣음
json_result["actual_name"] = args.file
json_result["hash_list"] = list
json_result["size"] = file_size

# Dictionary를 json.dumps를 이용하여 string으로 바꿈
json_object = json.dumps(json_result, indent=2)

# 해당 이름.simpletorrent 파일로 저장(w를 이용하여 스트링으로 저장)
with open(args.file + ".simpletorrent", "w") as output:
    output.write(json_object)
    output.close()
