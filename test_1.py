# import numpy as np
# import time
# import sys
# import datetime
# import os
# from scipy.sparse import csr_matrix
# import re
# import random
# import hashlib
# import hmac
# import random
# import pickle
# import pypbc
# import gmpy
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# import json
# import string
# from web3 import Web3
# from pypbc import *
# import gmpy2
# from gmpy2 import mpz
# from web3 import Web3
# import json
# from web3.middleware import geth_poa_middleware
# import struct
# from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
# model = AES.MODE_ECB
# BLOCK_SIZE=32
#
# skk = str(123456).encode('utf-8')
# b='ajsdghfjahlsd'.encode('utf-8')
# secreat_key = hmac.new(skk).digest()
# print('secreat_key', secreat_key)
# aes = AES.new(secreat_key, model)
# Enc_b = aes.encrypt(pad(b, BLOCK_SIZE))
# print('Enc_b',Enc_b)
# aes1 = AES.new(secreat_key, model)
# c=aes1.decrypt(Enc_b)
#
# print(unpad(c,BLOCK_SIZE))


# from socket import *
# HOST = '144.214.91.192'  # or 'localhost'
# PORT = 8001
# BUFSIZ = 1024
# ADDR = (HOST, PORT)
#
# tcpCliSock = socket(AF_INET, SOCK_STREAM)
# tcpCliSock.connect(ADDR)
# while True:
#     data1 = input('client>')
#     if not data1:
#         break
#     tcpCliSock.send(data1.encode())
#     data1 = tcpCliSock.recv(BUFSIZ)
#     if not data1:
#         break
#     print(data1)
# tcpCliSock.close()

import numpy as np
import time
import sys
import datetime
import os
from scipy.sparse import csr_matrix
import re
import random
import hashlib
import hmac
import random
import pickle
import pypbc
import gmpy
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json
import string
from web3 import Web3
from pypbc import *
import gmpy2
from gmpy2 import mpz
from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
import struct
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider

model = AES.MODE_ECB
BLOCK_SIZE = 32


def Initial(f_sensor_num, fog_num):
    p = get_random_prime(256)
    q = get_random_prime(256)
    n = p * q
    params = Parameters(n=p * q)
    pairing = Pairing(params)
    print('pairing',pairing)
    params1 = Parameters(n=p * q)
    pairing1 = Pairing(params1)
    print('pairing1', pairing)
    # 取两个生成元
    g = Element.random(pairing, G2)
    x = Element.random(pairing, G2)
    # 生成DO私钥
    DO_sk = Element.random(pairing, Zr)
    # 生成sensor的私钥,生成cloud存储index
    sensor_sk = {}
    cloud_store = {}
    for i in range(0, fog_num):
        for j in range(0, f_sensor_num):
            Sid = 'F' + str(i) + 'S' + str(j)
            cloud_store[Sid] = {}
            s = Element.random(pairing, Zr)
            # skk=hmac.new(b'chen').digest()
            # secreat_key = hmac.new(b'chen').digest()
            sensor_sk[Sid] = s
    # 生成fog的私钥和公钥
    fog_sk = []
    fog_pk = []
    for i in range(0, fog_num):
        sf = Element.random(pairing, Zr)
        pf = Element(pairing, G2, value=(g ** sf))
        fog_sk.append(sf)
        fog_pk.append(pf)
    # 生成cloud的私钥和公钥
    sk_c = p
    pk_c = Element(pairing, G2, value=(x ** q))
    # 生成registration ticket for each fog
    Res = {}
    for i in range(0, fog_num):
        Regis_set = {}
        for j in range(0, f_sensor_num):
            Sid = 'F' + str(i) + 'S' + str(j)
            # print(type(sensor_sk[Sid]),sensor_sk[Sid])
            k = sensor_sk[Sid].__invert__()
            # print('k:',k)
            inverse_sk = Element(pairing, Zr, value=k)
            Regis_set[Sid] = Element(pairing, G2, value=(g ** DO_sk) ** inverse_sk)
        Res[i] = Regis_set
    return g, x, DO_sk, sensor_sk, fog_sk, fog_pk, sk_c, pk_c, Res, pairing, cloud_store


def Enc_tag(b, d, g, pairing, pk_fog, sensorID, sensor_sk):
    sk_sensor = sensor_sk[sensorID]
    r = Element.random(pairing, Zr)
    t1 = Element(pairing, G2, value=(g ** r))
    tt = Element(pairing, G2, value=(pk_fog) ** r)
    kb = Web3.keccak(b)
    HashV = Element.from_hash(pairing, Zr, kb)
    # print('HashV',HashV)
    shb = sk_sensor * HashV
    skk = str(sk_sensor).encode('utf-8')
    secreat_key = hmac.new(skk).digest()
    print('secreat_key', secreat_key)
    aes = AES.new(secreat_key, model)
    Enc_b = aes.encrypt(pad(b, BLOCK_SIZE))
    Enc_d = aes.encrypt(pad(d, BLOCK_SIZE))
    sensor_data_send = [sensorID, Enc_b, Enc_d, t1, shb, tt]
    return sensor_data_send, HashV


def search(sensorID, t, cloud_store, basetable):
    sk = sensor_sk[sensorID]
    skk = str(sk).encode('utf-8')
    secreat_key = hmac.new(skk).digest()
    print('secreat_key', secreat_key)
    print('******')
    b_id, Enc_d = cloud_store[sensorID][t]
    Enc_b = basetable[b_id]
    aes1 = AES.new(secreat_key, model)
    b = unpad(aes1.decrypt(Enc_b), BLOCK_SIZE)
    d = unpad(aes1.decrypt(Enc_d), BLOCK_SIZE)
    return b, d


def dedup(Fog_receive, g, pairing, sk_fog, regis, I_fog, pk_c, I_cloud, cloud_store, basetable, time):
    for eachSD in Fog_receive:
        sensorID = eachSD[0]
        base = eachSD[1]
        deviation = eachSD[2]
        t1 = eachSD[3]
        shb = eachSD[4]
        tt = eachSD[5]
        reg = regis[sensorID]
        t1pie = Element(pairing, G2, value=(t1 ** sk_fog))
        k = t1pie.__invert__()
        k0 = Element(pairing, G2, value=k * tt)
        if k0 == 0:
            ft = Element(pairing, G2, value=(reg ** shb))
            print('ft', ft)
            linshift = str(ft)
            print('linshift', linshift)
        else:
            ftb = -1
            print('I cannot process it')
            return -1
        ####判断fog是否有重复数据
        if linshift in I_fog.keys():
            print('in the fog')
            base_ID = I_fog[linshift]
        else:
            ####判断cloud中是否有重复数据
            rb = Element.random(pairing, Zr)
            tag_c = Element(pairing, G2, value=(ft * (pk_c ** rb)))
            ####cloud检查是否存在index
            ct = Element(pairing, G2, value=(tag_c ** sk_c))
            linshict = str(ct)
            if linshict in I_cloud:
                print('in the cloud')
                base_ID = I_cloud[linshict]
                I_fog[linshift] = base_ID
            else:
                ####cloud没有存储，生成新的ID,存储base
                base_ID = str(random.randint(1000000, 9999999))
                I_cloud[linshict] = base_ID
                I_fog[linshift] = base_ID
                basetable[base_ID] = base
        ####存储
        cloud_store[sensorID][time] = [base_ID, deviation]
    return cloud_store, basetable


if __name__ == "__main__":
    f_sensor_num = 6
    fog_num = 2
    g, x, DO_sk, sensor_sk, fog_sk, fog_pk, sk_c, pk_c, Res, pairing, cloud_store=Initial(f_sensor_num, fog_num)
    print('pairing',pairing)
    kk=str(pairing)
    print(kk)
    gg=Pairing(pairing)
    print(gg)
    # f_groupp = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/g.txt',
    #                        mode='wb')
    # pickle.dump(str(g), f_groupp)
    # f_groupp.close()




    # g, x, DO_sk, sensor_sk, fog_sk, fog_pk, sk_c, pk_c, Res, pairing, cloud_store = recept

    ####获得base和deviation
    # f_str_basearray = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/str_basearray.txt',
    #                        mode='rb')
    # str_basearray = pickle.load(f_str_basearray)
    # f_str_deviationarray = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/str_deviationarray.txt',
    #                             mode='rb')
    # str_deviationarray = pickle.load(f_str_deviationarray)
    # Fog_receive = []
    # m = []
    # HashVset = []
    # for eline in range(0, 6):
    #     base = str_basearray[eline]
    #     deviation = str_deviationarray[eline]
    #     ###将base和deviation转成字节
    #     b_base = base.encode('utf-8')
    #     b_deviation = deviation.encode('utf-8')
    #     m.append(b_base)
    #     #####sensor加密数据并生成tag
    #     Sid = 'F' + str(0) + 'S' + str(eline)
    #     sensor_data_send, HashV = Enc_tag(b_base, b_deviation, g, pairing, fog_pk[0], Sid, sensor_sk)
    #     HashVset.append(HashV)
    #     Fog_receive.append(sensor_data_send)
    # ######################fog0和cloud执行去重
    # ###fog0的私钥和registration set
    # sk_fog = fog_sk[0]
    # regis = Res[0]
    # I_fog = {}
    # I_cloud = {}
    # basetable = {}
    # c_store, basetable = dedup(Fog_receive, g, pairing, sk_fog, regis, I_fog, pk_c, I_cloud, cloud_store, basetable, 1)
    # # print('c_store',c_store)
    # # print(len(basetable))
    # b, d = search('F0S0', 1, cloud_store, basetable)
    # print('b', b)
    # print('d', d)
    #
    #





