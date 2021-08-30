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
BLOCK_SIZE=32
def Initial(f_sensor_num, fog_num):
    p=get_random_prime(256)
    q=get_random_prime(256)
    n=p*q
    params=Parameters(n=p*q)
    pairing=Pairing(params)
    #取两个生成元
    g=Element.random(pairing, G2)
    x=Element.random(pairing, G2)
    # 生成DO私钥
    alpha=Element.random(pairing, Zr)
    gama=Element.random(pairing, Zr)
    y=Element(pairing, G2, value=( x ** q))
    v = Element(pairing, G2, value=(g ** gama))
    #生成g_i
    gg=[]
    g1=Element(pairing, G2, value=(g ** alpha))
    gg.append(g1)
    for i in range(1, 2*fog_num):
        g1=Element(pairing, G2, value=(g1 ** alpha))
        gg.append(g1)

    ########生成sensor私钥
    sensor_sk = {}
    fog_sk=[]
    fog_pk=[]
    cloud_store = {}
    Cloud_fog={}
    for i in range(0, fog_num):
        ## 每个fog生成私钥和公钥
        Cloud_fog[i]=[]
        linshif = Element.random(pairing, Zr)
        fog_sk.append(linshif)
        pkfog=Element(pairing, G2, value=(g ** linshif))
        fog_pk.append(pkfog)
        for j in range(0, f_sensor_num):
            Sid = 'F' + str(i) + 'S' + str(j)
            cloud_store[Sid] = {}
            sensor_sk[Sid]=Element(pairing, G2, value=(gg[i] ** gama))
    #生成cloud的私钥和公钥
    sk_c=p
    pk_c=y
    #生成registration ticket for each fog
    return g,x,sensor_sk,fog_sk,fog_pk,sk_c,pk_c,pairing,cloud_store,gg,v,Cloud_fog




def Enc_tag(b_data,g,pairing,pk_fog,sensorID,sensor_sk):
    sk_sensor = sensor_sk[sensorID]
    r = Element.random(pairing, Zr)
    t1=Element(pairing, G2, value=(g**r))
    kb = Web3.keccak(b_data)
    HashV = Element.from_hash(pairing, Zr, kb)
    t2=Element(pairing, G2, value=(sk_sensor**HashV)*(pk_fog**r))
    skk = str(sk_sensor).encode('utf-8')
    secreat_key = hmac.new(skk).digest()
    # print('secreat_key', secreat_key)
    aes = AES.new(secreat_key, model)
    Enc_data = aes.encrypt(pad(b_data, BLOCK_SIZE))
    # Enc_d = aes.encrypt(pad(d, BLOCK_SIZE))
    sensor_data_send=[sensorID,Enc_data,t1,t2]
    return sensor_data_send,HashV

def rangesensorenc(Batchdata, g, pairing, pk_fog, sensorID, sensor_sk):
    Fog_rev=[]
    for i in range(0, len(Batchdata)):
        b_data = Batchdata[i]
        sk_sensor = sensor_sk[sensorID]
        r = Element.random(pairing, Zr)
        t1 = Element(pairing, G2, value=(g ** r))
        kb = Web3.keccak(b_data)
        HashV = Element.from_hash(pairing, Zr, kb)
        t2 = Element(pairing, G2, value=(sk_sensor ** HashV) * (pk_fog ** r))
        skk = str(sk_sensor).encode('utf-8')
        secreat_key = hmac.new(skk).digest()
        # print('secreat_key', secreat_key)
        aes = AES.new(secreat_key, model)
        Enc_data = aes.encrypt(pad(b_data, BLOCK_SIZE))
        # Enc_d = aes.encrypt(pad(d, BLOCK_SIZE))
        sensor_data_send = [sensorID, Enc_data, t1, t2]
        Fog_rev.append(sensor_data_send)
    return Fog_rev

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




        # Fog_receive, g, pairing, sk_fog, I_fog, pk_c, sk_c, I_cloud, cloud_store, basetable, 1,Cloud_fog, 4, 0, gg
def fog_dedup(Fog_receive,g,pairing,sk_fog,I_fog,pk_c,basetable,time):
    print('len(Fog_receive)',len(Fog_receive))
    cloud_rev_data=[]
    for eachSD in Fog_receive:
        # [sensorID, Enc_b, Enc_d, t1, t2]
        sensorID = eachSD[0]
        data = eachSD[1]
        # deviation = eachSD[2]
        t1 = eachSD[2]
        t2 = eachSD[3]
        # tt = eachSD[5]
        # reg=regis[sensorID]
        t1pie=Element(pairing, G2, value=(t1**sk_fog))
        k = t1pie.__invert__()
        ft=Element(pairing, G2, value=t2*k)
        # print('ft', ft)
        linshift = str(ft)
        # print('linshift', linshift)
        ####判断fog是否有重复数据
        if linshift in I_fog.keys():
            print('in the fog')
            base_ID=I_fog[linshift]
        else:
            ####判断cloud中是否有重复数据(和不是同意fog的数据进行比较)
            rb = Element.random(pairing, Zr)
            tag_c = Element(pairing, G2, value=(ft * (pk_c ** rb)))
            data1=[tag_c, linshift, sensorID]
            cloud_rev_data.append(data1)

            ####cloud检查是否存在index

    return cloud_rev_data

def store_in_cloud(cloud_rev_data,cipher_fog_number, total_fog_num,I_fog,Cloud_fog,gg,sk_c,cloud_store,basetable):
    for data in cloud_rev_data:
        tag_c = data[0]
        linshift = data[1]
        sensorID = data[2]
        # print('cipher_fog_number', cipher_fog_number)
        # print('total_fog_num', total_fog_num)
        dataID = I_cloud[str(tag_c)]
        I_fog[linshift] = dataID
        Cloud_fog[cipher_fog_number].append(tag_c)
        base_ID = str(random.randint(1000000, 9999999))
        I_cloud[str(tag_c)] = base_ID
        basetable[base_ID] = data
        cloud_store[sensorID][time] = [base_ID]
    return cloud_store, basetable


def cloud_dedu(cloud_rev_data,cipher_fog_number, total_fog_num,I_fog,Cloud_fog,gg,sk_c,cloud_store,basetable):
    for data in cloud_rev_data:
        tag_c=data[0]
        linshift=data[1]
        sensorID=data[2]
        # print('cipher_fog_number', cipher_fog_number)
        # print('total_fog_num', total_fog_num)
        check = 0
        for i in range(0, total_fog_num):
            # print('i', i)
            if i != cipher_fog_number:
                # print('****')
                # print('Cloud_fog[i]',Cloud_fog[i])
                # print('cipher_fog_number',cipher_fog_number)
                list_needcompare = Cloud_fog[i]
                # print('list_needcompare', len(list_needcompare))
                if len(list_needcompare)>0:
                    pairtag_c = pairing.apply(tag_c, gg[i])
                    pairtag_c_p = Element(pairing, GT, value=(pairtag_c ** sk_c))
                    for eachitem in list_needcompare:
                        pairing_test = pairing.apply(eachitem, gg[cipher_fog_number])
                        pairing_test_p = Element(pairing, GT, value=(pairing_test ** sk_c))
                        # print('pairing_test_p', pairing_test_p)
                        if pairtag_c_p == pairing_test_p:
                            print('in the cloud')
                            dataID = I_cloud[str(tag_c)]
                            I_fog[linshift] = dataID
                            check = 1
                            break
        # print('check', check)
        if check == 0:
            Cloud_fog[cipher_fog_number].append(tag_c)
            # print('Cloud_fog[cipher_fog_number]', len(Cloud_fog[cipher_fog_number]))
            base_ID = str(random.randint(1000000, 9999999))
            I_cloud[str(tag_c)] = base_ID
            I_fog[linshift] = base_ID
            basetable[base_ID] = data
        ####存储
    cloud_store[sensorID][time] = [base_ID]
    return cloud_store,basetable, Cloud_fog








if __name__=="__main__":
    f_sensor_num=6
    fog_num=2

    g,x,sensor_sk,fog_sk,fog_pk,sk_c,pk_c,pairing,cloud_store,gg,v,Cloud_fog=Initial(f_sensor_num, fog_num)
    ####获得base和deviation
    f_str_basearray = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/str_basearray.txt',mode='rb')
    str_basearray = pickle.load(f_str_basearray)
    f_str_deviationarray = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/str_deviationarray.txt',mode='rb')
    str_deviationarray = pickle.load(f_str_deviationarray)
    m=[]
    HashVset=[]
    Batchdata=[]
    Sid = 'F' + str(0) + 'S' + str(1)
    for eline in range(0,2500):
        data=str_basearray[eline]+str_deviationarray[eline]
        # base=str_basearray[eline]
        # deviation=str_deviationarray[eline]
        ###将数据转成字节
        b_data=data.encode('utf-8')
        # b_deviation=deviation.encode('utf-8')
        m.append(b_data)
        #####sensor加密数据并生成tag
        # sensor_data_send,HashV=Enc_tag(b_data,g,pairing,fog_pk[0],Sid,sensor_sk)
        # HashVset.append(HashV)
        Batchdata.append(b_data)
        # Fog_receive.append(sensor_data_send)
    print('len(Batchdata)',len(Batchdata))
    Fog_receive=rangesensorenc(Batchdata, g, pairing, fog_pk[0], Sid, sensor_sk)
    ######################fog0和cloud执行去重
    ###fog0的私钥和registration set
    sk_fog = fog_sk[0]
    I_fog={}
    I_cloud={}
    basetable={}
    # Fog_receive, g, pairing, sk_fog, regis, I_fog, pk_c, sk_c, I_cloud, cloud_store, basetable, time, Cloud_fog, total_fog_num, cipher_fog_number, gg
    # c_store,basetable=dedup(Fog_receive, g, pairing, sk_fog, I_fog, pk_c, sk_c, I_cloud, cloud_store, basetable, 1,Cloud_fog, fog_num, 0, gg)
    cloud_rev_data=fog_dedup(Fog_receive, g, pairing, sk_fog, I_fog, pk_c, basetable, time)
    cloud_store,basetable=store_in_cloud(cloud_rev_data, 0, 2, I_fog, Cloud_fog, gg, sk_c,cloud_store,basetable)

    Batchdata=[]
    for eline in range(2500, 5000):
        data = str_basearray[eline] + str_deviationarray[eline]
        # base=str_basearray[eline]
        # deviation=str_deviationarray[eline]
        ###将数据转成字节
        b_data = data.encode('utf-8')
        # b_deviation=deviation.encode('utf-8')
        m.append(b_data)
        #####sensor加密数据并生成tag
        # sensor_data_send,HashV=Enc_tag(b_data,g,pairing,fog_pk[0],Sid,sensor_sk)
        # HashVset.append(HashV)
        Batchdata.append(b_data)
        # Fog_receive.append(sensor_data_send)
    print('len(Batchdata)', len(Batchdata))
    Fog_receive = rangesensorenc(Batchdata, g, pairing, fog_pk[0], Sid, sensor_sk)
    cloud_rev_data = fog_dedup(Fog_receive, g, pairing, sk_fog, I_fog, pk_c, basetable, time)
    start1 = datetime.datetime.now()
    cloud_store, basetable,Cloud_fog = cloud_dedu(cloud_rev_data, 1, 2, I_fog, Cloud_fog, gg, sk_c,cloud_store,basetable)
    end1 = datetime.datetime.now()
    print('cloud-lelvel deduplication time2', end1 - start1)

