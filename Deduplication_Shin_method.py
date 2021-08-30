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
import datetime
model = AES.MODE_ECB
BLOCK_SIZE=32
import math
def Initial(f_sensor_num, fog_num):
    p=get_random_prime(256)
    q=get_random_prime(256)
    n=p*q
    params=Parameters(n=p*q)
    pairing=Pairing(params)
    #取生成元
    g=Element.random(pairing, G2)
    ########生成sensor私钥
    # sensor_sk = {}
    fog_sk=[]
    fog_pk=[]
    cloud_store = {}
    Cloud_fog={}
    for i in range(0, fog_num):
        ## 每个fog生成私钥和公钥
        x=Element.random(pairing, Zr)
        y = Element.random(pairing, Zr)
        yni= y.__invert__()
        pk1=Element(pairing, G2, value=(g ** x))
        pk2=Element(pairing, G2, value=(g ** y))
        pk3=Element(pairing, G2, value=(g ** yni))
        pk=[pk1,pk2,pk3]
        sk=[x,y]
        fog_pk.append(pk)
        fog_sk.append(sk)
        for j in range(0, f_sensor_num):
            Sid = 'F' + str(i) + 'S' + str(j)
            cloud_store[Sid] = {}
    return g,x,fog_sk,fog_pk,pairing,cloud_store,Cloud_fog



def rangesensor_enc(Batch_data, g, pairing):
    Fog_receive=[]
    for i in range(0,len(Batch_data)):
        kb = Web3.keccak(Batch_data[i])
        h=Element.from_hash(pairing, G2, kb)
        x = Element.random(pairing, Zr)
        y = Element.random(pairing, Zr)
        r1 = Element.random(pairing, Zr)
        r2 = Element.random(pairing, Zr)
        theta=Element(pairing, G2, value=((g ** r1) * h))
        tao = Element(pairing, G2, value=((g ** r2) * h))
        D=[h,theta,tao,r1,r2]
        Fog_receive.append(D)
    return Fog_receive



def inter_dedu(Fog_receive, g, pairing,pk_,I_fog, fog_number):
    pk0=pk_[0]
    pk1=pk_[1]
    cloud_rev_data=[]
    for eachSD in Fog_receive:
        check=0
        ##拿数据
        h=eachSD[0]
        theta=eachSD[1]
        tao=eachSD[2]
        r1=eachSD[3]
        r2=eachSD[4]
        ##计算
        r1ni=r1.__invert__()
        r2ni=r2.__invert__()
        tf=Element(pairing, G2, value=(theta *(pk0**r1ni)))
        strtf=str(tf)
        ck_f=Element(pairing, G2, value=(tao* (pk0**r2ni)))
        for i in range(0,math.ceil(np.log2(3000))):
            if strtf in I_fog.keys():
                print('in the fog')
                base_ID=I_fog[strtf]
                check=1
        if check==0:
            data=[tf,fog_number]
            cloud_rev_data.append(data)
    return cloud_rev_data

def cloud_dedu(cloud_rev_data, S_all_num, chushu, g,pairing,fog_pk,Batch_data):
    for data in cloud_rev_data:
        tf=data[0]
        fog_number=data[1]
        kb = Web3.keccak(Batch_data[0])
        h = Element.from_hash(pairing, G2, kb)
        x = Element.random(pairing, Zr)
        for i in range(0, math.ceil(S_all_num/chushu)):
            t1=Element(pairing, G2, value=(tf*fog_pk[0][0]))
            t2=Element(pairing, G2, value=(tf*fog_pk[fog_number][0]))
            base_ID = str(random.randint(1000000, 9999999))
            I_cloud[str(t1)]=base_ID
            # print('**')
            if t1==t2:
                c=1
        S_all_num=S_all_num+1
    return I_cloud





#
#
#
#
# def Enc_tag(b_data,g,pairing,pk_fog,sensorID,sensor_sk):
#     sk_sensor = sensor_sk[sensorID]
#     r = Element.random(pairing, Zr)
#     t1=Element(pairing, G2, value=(g**r))
#     kb = Web3.keccak(b_data)
#     HashV = Element.from_hash(pairing, Zr, kb)
#     t2=Element(pairing, G2, value=(sk_sensor**HashV)*(pk_fog**r))
#     skk = str(sk_sensor).encode('utf-8')
#     secreat_key = hmac.new(skk).digest()
#     # print('secreat_key', secreat_key)
#     aes = AES.new(secreat_key, model)
#     Enc_data = aes.encrypt(pad(b_data, BLOCK_SIZE))
#     # Enc_d = aes.encrypt(pad(d, BLOCK_SIZE))
#     sensor_data_send=[sensorID,Enc_data,t1,t2]
#     return sensor_data_send,HashV



# def search(sensorID,t,cloud_store,basetable):
#     sk = sensor_sk[sensorID]
#     skk = str(sk).encode('utf-8')
#     secreat_key = hmac.new(skk).digest()
#     print('secreat_key',secreat_key)
#     print('******')
#     b_id,Enc_d=cloud_store[sensorID][t]
#     Enc_b=basetable[b_id]
#     aes1 = AES.new(secreat_key, model)
#     b = unpad(aes1.decrypt(Enc_b),BLOCK_SIZE)
#     d = unpad(aes1.decrypt(Enc_d),BLOCK_SIZE)
#     return b,d




#
#         # Fog_receive, g, pairing, sk_fog, I_fog, pk_c, sk_c, I_cloud, cloud_store, basetable, 1,Cloud_fog, 4, 0, gg
# def dedup(Fog_receive,g,pairing,sk_fog,I_fog,pk_c,sk_c,I_cloud,cloud_store,basetable,time,Cloud_fog,total_fog_num,cipher_fog_number,gg):
#     print('len(Fog_receive)',len(Fog_receive))
#     for eachSD in Fog_receive:
#         # [sensorID, Enc_b, Enc_d, t1, t2]
#         sensorID = eachSD[0]
#         data = eachSD[1]
#         # deviation = eachSD[2]
#         t1 = eachSD[2]
#         t2 = eachSD[3]
#         # tt = eachSD[5]
#         # reg=regis[sensorID]
#         t1pie=Element(pairing, G2, value=(t1**sk_fog))
#         k = t1pie.__invert__()
#         ft=Element(pairing, G2, value=t2*k)
#         print('ft', ft)
#         linshift = str(ft)
#         # print('linshift', linshift)
#         ####判断fog是否有重复数据
#         if linshift in I_fog.keys():
#             print('in the fog')
#             base_ID=I_fog[linshift]
#         else:
#             ####判断cloud中是否有重复数据(和不是同意fog的数据进行比较)
#             rb = Element.random(pairing, Zr)
#             tag_c = Element(pairing, G2, value=(ft * (pk_c ** rb)))
#             ####cloud检查是否存在index
#             check=0
#             print('cipher_fog_number',cipher_fog_number)
#             print('total_fog_num',total_fog_num)
#             for i in range(0,total_fog_num):
#                 print('i',i)
#                 if i!=cipher_fog_number:
#                     pairtag_c=pairing.apply(tag_c,gg[i])
#                     pairtag_c_p=Element(pairing, GT, value=(pairtag_c ** sk_c))
#                     list_needcompare = Cloud_fog[i]
#                     print('list_needcompare',len(list_needcompare))
#                     for eachitem in list_needcompare:
#                         pairing_test=pairing.apply(eachitem,gg[cipher_fog_number])
#                         pairing_test_p=Element(pairing, GT, value=(pairing_test ** sk_c))
#                         print('pairing_test_p',pairing_test_p)
#                         if pairtag_c_p==pairing_test_p:
#                             print('in the cloud')
#                             dataID=I_cloud[str(tag_c)]
#                             I_fog[linshift]= dataID
#                             check=1
#                             break
#             print('check',check)
#             if check==0:
#                 Cloud_fog[cipher_fog_number].append(tag_c)
#                 print('Cloud_fog[cipher_fog_number]',len(Cloud_fog[cipher_fog_number]))
#                 base_ID = str(random.randint(1000000, 9999999))
#                 I_cloud[str(tag_c)] = base_ID
#                 I_fog[linshift] = base_ID
#                 basetable[base_ID] = data
#         ####存储
#         cloud_store[sensorID][time]=[base_ID]
#     return cloud_store,basetable










if __name__=="__main__":
    f_sensor_num=6
    fog_num=2

    g,x,fog_sk,fog_pk,pairing,cloud_store,Cloud_fog=Initial(f_sensor_num, fog_num)
    ####获得base和deviation
    f_str_basearray = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/str_basearray.txt',mode='rb')
    str_basearray = pickle.load(f_str_basearray)
    f_str_deviationarray = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/str_deviationarray.txt',mode='rb')
    str_deviationarray = pickle.load(f_str_deviationarray)
    Fog_receive=[]
    m=[]
    HashVset=[]
    Sid = 'F' + str(0) + 'S' + str(1)
    Batch_data=[]

    for eline in range(0,5000):
        data=str_basearray[eline]+str_deviationarray[eline]
        ###将数据转成字节
        b_data=data.encode('utf-8')
        #####sensor加密数据并生成tag
        Batch_data.append(b_data)
    Fog_receive=rangesensor_enc(Batch_data,g,pairing)
    ######################fog0和cloud执行去重
    ###fog0的私钥和registration set
    I_fog={}
    I_cloud={}
    basetable={}
    # start1=datetime.datetime.now()
    cloud_rev_data=inter_dedu(Fog_receive, g, pairing,fog_pk[0],I_fog,0)
    # inter_dedu(Fog_receive, g, pairing, pk_, I_fog, fog_number):

    start1 = datetime.datetime.now()
    cloud_dedu(cloud_rev_data, 0, 32, g, pairing, fog_pk,Batch_data)
    end1 = datetime.datetime.now()
    print('cloud_dedu time cost====', end1 - start1)

    Batch_data = []
    for eline in range(5000,5100):
        data=str_basearray[eline]+str_deviationarray[eline]
        ###将数据转成字节
        b_data=data.encode('utf-8')
        #####sensor加密数据并生成tag
        Batch_data.append(b_data)
    Fog_receive=rangesensor_enc(Batch_data,g,pairing)
    ######################fog0和cloud执行去重
    ###fog0的私钥和registration set
    # start1=datetime.datetime.now()
    cloud_rev_data=inter_dedu(Fog_receive, g, pairing,fog_pk[0],I_fog,0)
    # inter_dedu(Fog_receive, g, pairing, pk_, I_fog, fog_number):

    start1 = datetime.datetime.now()
    cloud_dedu(cloud_rev_data, 0, 32, g, pairing, fog_pk,Batch_data)
    end1 = datetime.datetime.now()
    print('cloud_dedu time cost1---1', end1 - start1)

    Batch_data = []
    for eline in range(5100,5200):
        data=str_basearray[eline]+str_deviationarray[eline]
        ###将数据转成字节
        b_data=data.encode('utf-8')
        #####sensor加密数据并生成tag
        Batch_data.append(b_data)
    Fog_receive=rangesensor_enc(Batch_data,g,pairing)
    ######################fog0和cloud执行去重
    ###fog0的私钥和registration set
    # start1=datetime.datetime.now()
    cloud_rev_data=inter_dedu(Fog_receive, g, pairing,fog_pk[0],I_fog,0)
    # inter_dedu(Fog_receive, g, pairing, pk_, I_fog, fog_number):

    start1 = datetime.datetime.now()
    cloud_dedu(cloud_rev_data, 0, 32, g, pairing, fog_pk,Batch_data)
    end1 = datetime.datetime.now()
    print('cloud_dedu time cost====2', end1 - start1)

    Batch_data = []
    for eline in range(5200,5300):
        data=str_basearray[eline]+str_deviationarray[eline]
        ###将数据转成字节
        b_data=data.encode('utf-8')
        #####sensor加密数据并生成tag
        Batch_data.append(b_data)
    Fog_receive=rangesensor_enc(Batch_data,g,pairing)
    ######################fog0和cloud执行去重
    ###fog0的私钥和registration set
    I_fog={}
    I_cloud={}
    basetable={}
    # start1=datetime.datetime.now()
    cloud_rev_data=inter_dedu(Fog_receive, g, pairing,fog_pk[0],I_fog,0)
    # inter_dedu(Fog_receive, g, pairing, pk_, I_fog, fog_number):

    start1 = datetime.datetime.now()
    cloud_dedu(cloud_rev_data, 0, 32, g, pairing, fog_pk,Batch_data)
    end1 = datetime.datetime.now()
    print('cloud_dedu time cost====3', end1 - start1)



    Batch_data = []
    for eline in range(5300,5400):
        data=str_basearray[eline]+str_deviationarray[eline]
        ###将数据转成字节
        b_data=data.encode('utf-8')
        #####sensor加密数据并生成tag
        Batch_data.append(b_data)
    Fog_receive=rangesensor_enc(Batch_data,g,pairing)
    ######################fog0和cloud执行去重
    ###fog0的私钥和registration set
    I_fog={}
    I_cloud={}
    basetable={}
    # start1=datetime.datetime.now()
    cloud_rev_data=inter_dedu(Fog_receive, g, pairing,fog_pk[0],I_fog,0)
    # inter_dedu(Fog_receive, g, pairing, pk_, I_fog, fog_number):

    start1 = datetime.datetime.now()
    cloud_dedu(cloud_rev_data, 0, 32, g, pairing, fog_pk,Batch_data)
    end1 = datetime.datetime.now()
    print('cloud_dedu time cost====4', end1 - start1)

    Batch_data = []
    for eline in range(5400,5500):
        data=str_basearray[eline]+str_deviationarray[eline]
        ###将数据转成字节
        b_data=data.encode('utf-8')
        #####sensor加密数据并生成tag
        Batch_data.append(b_data)
    Fog_receive=rangesensor_enc(Batch_data,g,pairing)
    ######################fog0和cloud执行去重
    ###fog0的私钥和registration set
    I_fog={}
    I_cloud={}
    basetable={}
    # start1=datetime.datetime.now()
    cloud_rev_data=inter_dedu(Fog_receive, g, pairing,fog_pk[0],I_fog,0)
    # inter_dedu(Fog_receive, g, pairing, pk_, I_fog, fog_number):

    start1 = datetime.datetime.now()
    cloud_dedu(cloud_rev_data, 0, 32, g, pairing, fog_pk,Batch_data)
    end1 = datetime.datetime.now()
    print('cloud_dedu time cost====5', end1 - start1)

