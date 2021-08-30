# -*- coding: utf-8 -*-

import zlib
from AEScoder import AEScode
from cnRedis import ConnRedis


def baseline_put(r, aes_code, index, plaintext):
    compressed_bytes = zlib.compress(plaintext.encode('utf-8'))
    print(compressed_bytes)
    encrypted_line = aes_code.encrypt(str(compressed_bytes))
    print(encrypted_line)
    r.put(index, encrypted_line)


def baseline_single_get(r, aes_code, index):
    global list
    re = r.single_get(index)

    decrypt_line = aes_code.decrypt(re[0])
    print(re[0])
    print(decrypt_line)

    decompress_bytes = zlib.decompress(decrypt_line)
    print(decompress_bytes)


def baseline_range_get(r, low, up):
    re = r.range_get(low, up)
    result = []
    aes_code = AEScode()
    decrypt_line = aes_code.decrypt(re)
    decompress_bytes = zlib.decompress(bytes(decrypt_line, encoding="utf8"))
    print(decompress_bytes.decode('utf-8'))


def baseline_delete(r, index):
    re = r.delete(index)
    return re


def initialize(conn_redis, aes_code):
    with open("dataset/inFileExample", "r") as f:
        data = f.readlines()
        ind = 1
        for line in data:
            line = line.strip('\n').replace('\t', ' ')
            line_str = line.split(' ')

            line_pair = [x for x in line_str if x != '' and x != '10']

            pre_compress = ",".join(line_pair)
            # print(pre_compress)

            com_bytes = zlib.compress(pre_compress.encode('utf-8'))
            # print(type(com_bytes))
            # decompress_bytes = zlib.decompress(com_bytes)
            # print(decompress_bytes.decode('utf-8'))

            encrypted_line = aes_code.encrypt(str(com_bytes))
            # print(encrypted_line)

            # decrypt_line = aes_code.decrypt(encrypt_line)
            # print(decrypt_line)
            print(ind, encrypted_line)
            conn_redis.put(ind, encrypted_line)

            ind += 1


if __name__ == '__main__':
    conn_redis = ConnRedis()
    aes_code = AEScode()
    initialize(conn_redis, aes_code)

    print('initialize completed')
    index = 285
    test_string = '80:ea:11:ad:77:12,608'

    baseline_put(conn_redis, aes_code, index, test_string)
    baseline_single_get(conn_redis, aes_code, 285)