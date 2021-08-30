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
import copy
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
    #生成DO私钥
    DO_sk=Element.random(pairing, Zr)
    #生成sensor的私钥,生成cloud存储index
    sensor_sk={}
    cloud_store={}
    for i in range(0,fog_num):
        for j in range(0,f_sensor_num):
            Sid='F'+str(i)+'S'+str(j)
            cloud_store[Sid]={}
            s = Element.random(pairing, Zr)
            # skk=hmac.new(b'chen').digest()
            # secreat_key = hmac.new(b'chen').digest()
            sensor_sk[Sid]=s
    #生成fog的私钥和公钥
    fog_sk=[]
    fog_pk=[]
    for i in range(0, fog_num):
        sf=Element.random(pairing, Zr)
        pf=Element(pairing, G2, value=(g ** sf))
        fog_sk.append(sf)
        fog_pk.append(pf)
    #生成cloud的私钥和公钥
    sk_c=p
    pk_c=Element(pairing, G2, value=(x ** q))
    #生成registration ticket for each fog
    Res={}
    for i in range(0,fog_num):
        Regis_set={}
        for j in range(0, f_sensor_num):
            Sid = 'F' + str(i) + 'S' + str(j)
            # print(type(sensor_sk[Sid]),sensor_sk[Sid])
            # k=sensor_sk[Sid].__invert__()
            # # print('k:',k)
            # inverse_sk = Element(pairing, Zr, value=k)
            # Regis_set[Sid]=Element(pairing, G2, value=(g ** DO_sk) ** inverse_sk)

            Regis_set[Sid] = Element(pairing, G2, value=g**(DO_sk-sensor_sk[Sid]))
        Res[i]=Regis_set
    return g,x,DO_sk,sensor_sk,fog_sk,fog_pk,sk_c,pk_c,Res,pairing,cloud_store





def Enc_tag(b,d,g,pairing,pk_fog,sensorID,sensor_sk):
    sk_sensor = sensor_sk[sensorID]
    r = Element.random(pairing, Zr)
    t1=Element(pairing, G2, value=(g**r))
    kb = Web3.keccak(b)
    HashV = Element.from_hash(pairing, Zr, kb)
    t2=Element(pairing, G2, value=(g**sk_sensor)*(g**HashV)*(pk_fog**r))

    # tt=Element(pairing, G2, value=(pk_fog)**r)
    # print('HashV',HashV)
    skk = str(sk_sensor).encode('utf-8')
    secreat_key = hmac.new(skk).digest()
    # print('secreat_key', secreat_key)
    aes = AES.new(secreat_key, model)
    Enc_b = aes.encrypt(pad(b, BLOCK_SIZE))
    Enc_d = aes.encrypt(pad(d, BLOCK_SIZE))
    sensor_data_send=[sensorID,Enc_b,Enc_d,t1,t2]
    return sensor_data_send,HashV



def search(sensorID,t,cloud_store,basetable):
    sk = sensor_sk[sensorID]
    skk = str(sk).encode('utf-8')
    secreat_key = hmac.new(skk).digest()
    # print('secreat_key',secreat_key)
    # print('******')
    b_id,Enc_d=cloud_store[sensorID][t]
    Enc_b=basetable[b_id]
    print('len(Enc_b)',len(Enc_b))
    aes1 = AES.new(secreat_key, model)
    b = unpad(aes1.decrypt(Enc_b),BLOCK_SIZE)
    d = unpad(aes1.decrypt(Enc_d),BLOCK_SIZE)
    return b,d

def Batch_search(k,cloud_store,basetable,sensorID):
    encdata=[]
    for data in k:
        m=cloud_store[sensorID]
        b_id=data[0]
        Enc_d=data[1]
        Enc_b = basetable[b_id]
        # print('len(Enc_d)',len(Enc_d))
        # print('len(Enc_b)', len(Enc_b))
        encdata.append([Enc_b,Enc_d])
    return encdata


def DO_decry(sensor_sk,sensorID,encdata):
    sk_sensor = sensor_sk[sensorID]
    skk = str(sk_sensor).encode('utf-8')
    secreat_key = hmac.new(skk).digest()
    dataDe=[]
    for data in encdata:
        Enc_b=data[0]
        Enc_d=data[1]
        aes1 = AES.new(secreat_key, model)
        b = unpad(aes1.decrypt(Enc_b), BLOCK_SIZE)
        d = unpad(aes1.decrypt(Enc_d), BLOCK_SIZE)
        dataDe.append([b,d])
    return dataDe




def data_re_trans(dataDe, deviation):
    t=[]
    print('len(dataDe)##########',len(dataDe))
    for data in dataDe:
        b=(data[0].decode()).split()
        d=(data[1].decode()).split()
        for i in range(0,len(d)):
            b.insert(deviation[i],d[i])
        t.append(b)
    return t








def dedup(Fog_receive,g,pairing,sk_fog,regis,I_fog,pk_c,time):
    cloud_rev_data=[]
    for eachSD in Fog_receive:
        # [sensorID, Enc_b, Enc_d, t1, t2]
        sensorID = eachSD[0]
        base = eachSD[1]
        deviation = eachSD[2]
        t1 = eachSD[3]
        t2 = eachSD[4]
        # tt = eachSD[5]
        reg=regis[sensorID]
        t1pie=Element(pairing, G2, value=(t1**sk_fog))
        k = t1pie.__invert__()
        # k0=Element(pairing, G2, value=t2*k)
        # ft=Element(pairing, G2, value=(reg*k0))
        ft = Element(pairing, G2, value=(reg * (t2*k)))
        # print('ft', ft)
        linshift = str(ft)
        # print('linshift', linshift)
        ####判断fog是否有重复数据
        if linshift in I_fog.keys():
            # print('in the fog')
            base_ID=I_fog[linshift]
        else:
            ####判断cloud中是否有重复数据
            rb = Element.random(pairing, Zr)
            tag_c=Element(pairing, G2, value=(ft*(pk_c**rb)))
            I_fog[linshift]='1'
            data1=[tag_c,linshift,sensorID,deviation]
            cloud_rev_data.append(data1)
            ####cloud检查是否存在index
            # ct=Element(pairing, G2, value=(tag_c**sk_c))
            # linshict=str(ct)
        ###################################cloud side operation
        #     if linshict in I_cloud:
        #         print('in the cloud')
        #         base_ID=I_cloud[linshict]
        #         I_fog[linshift] = base_ID
        #     else:
        #         ####cloud没有存储，生成新的ID,存储base
        #         base_ID=str(random.randint(1000000,9999999))
        #         I_cloud[linshict]=base_ID
        #         I_fog[linshift]=base_ID
        #         basetable[base_ID]=base
        # ####存储
        # cloud_store[sensorID][time]=[base_ID,deviation]
    return cloud_rev_data


def cloud_layer_dedu(cloud_rev_data, I_cloud, I_fog,cloud_store,time,basetable):
    k=[]
    for data in cloud_rev_data:
        tag_c=data[0]
        linshift=data[1]
        sensorID=data[2]
        deviation=data[3]
        ct=Element(pairing, G2, value=(tag_c**sk_c))
        linshict=str(ct)
        ##################################cloud side operation
        if linshict in I_cloud:
            print('in the cloud')
            base_ID=I_cloud[linshict]
            I_fog[linshift] = base_ID
            cloud_store[sensorID][time] = [base_ID, deviation]
            k.append([base_ID, deviation])
        else:
            ####cloud没有存储，生成新的ID,存储base
            base_ID=str(random.randint(1000000,9999999))
            I_cloud[linshict]=base_ID
            I_fog[linshift]=base_ID
            basetable[base_ID]=base
            k.append([base_ID,deviation])
    ####存储
    return cloud_store, basetable, I_cloud, I_fog, k



def rangesensorenc(Batch_base, Batch_deviation, g, pairing, pk_fog, sensorID, sensor_sk):
    Fog_rev=[]
    achievemi=[]
    for i in range(0, len(Batch_base)):
        b = Batch_base[i]
        d = Batch_deviation[i]
        sk_sensor = sensor_sk[sensorID]
        r = Element.random(pairing, Zr)
        t1 = Element(pairing, G2, value=(g ** r))
        kb = Web3.keccak(b)
        HashV = Element.from_hash(pairing, Zr, kb)
        t2 = Element(pairing, G2, value=(g ** sk_sensor) * (g ** HashV) * (pk_fog ** r))
        skk = str(sk_sensor).encode('utf-8')
        secreat_key = hmac.new(skk).digest()
        aes = AES.new(secreat_key, model)
        Enc_b = aes.encrypt(pad(b, BLOCK_SIZE))
        Enc_d = aes.encrypt(pad(d, BLOCK_SIZE))
        achievemi.append([Enc_b,Enc_d])
        sensor_data_send = [sensorID, Enc_b, Enc_d, t1, t2]
        Fog_rev.append(sensor_data_send)
    return Fog_rev,achievemi




if __name__=="__main__":
    f_sensor_num=6
    fog_num=2

    g,x,DO_sk,sensor_sk,fog_sk,fog_pk,sk_c,pk_c,Res,pairing,cloud_store=Initial(f_sensor_num, fog_num)
    ####获得base和deviation
    f_str_basearray = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/str_basearray.txt',
                           mode='rb')
    #str_basearray_dataset2
    str_basearray = pickle.load(f_str_basearray)
    f_str_deviationarray = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/str_deviationarray.txt',
                                mode='rb')
    # str_deviationarray_dataset2

    #
    #
    # f_indextodelete = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/index_to_delete_dataset2.txt',
    #                        mode='rb')
    # Dev = pickle.load(f_indextodelete)


    str_deviationarray = pickle.load(f_str_deviationarray)
    Fog_receive=[]
    m=[]
    HashVset=[]
    #############################sensor process range data
    Batch_base = []
    Batch_deviation = []
    Sid = 'F' + str(0) + 'S' + str(1)
    for eline in range(0, 6000):
        base = str_basearray[eline]
        deviation = str_deviationarray[eline]
        ###将base和deviation转成字节
        b_base = base.encode('utf-8')
        b_deviation = deviation.encode('utf-8')
        print('type of b_deviation', type(b_deviation))
        m.append(b_base)
        #####sensor加密数据并生成tag
        # Sid = 'F' + str(0) + 'S' + str(eline)
        Batch_base.append(b_base)
        Batch_deviation.append(b_deviation)
    print('len(Batch_base)', len(Batch_base))
    start1 = datetime.datetime.now()
    Fog_rev,achievemi=rangesensorenc(Batch_base, Batch_deviation, g, pairing, fog_pk[0], Sid, sensor_sk)


    #####################fog0和cloud执行去重
    ##fog0的私钥和registration set
    sk_fog = fog_sk[0]
    regis = Res[0]
    I_fog={}
    I_cloud={}
    basetable={}
    start1 = datetime.datetime.now()
    cloud_rev_data=dedup(Fog_rev, g, pairing, sk_fog, regis, I_fog, pk_c, 1)
    end1 = datetime.datetime.now()
    print('fog-lelvel deduplication time', end1 - start1)
    print('still base', len(cloud_rev_data))
    # start1 = datetime.datetime.now()
    # cloud_store, basetable,I_cloud,I_fog,k=cloud_layer_dedu(cloud_rev_data, I_cloud, I_fog, cloud_store, 1,basetable)
    # end1 = datetime.datetime.now()
    # print('cloud-lelvel deduplication time', end1 - start1)
    # start1 = datetime.datetime.now()
    # encdata=Batch_search(k,cloud_store, basetable,Sid)
    # end1 = datetime.datetime.now()
    # print('cloud search time', end1 - start1)
    # print(len(encdata))
    # start1 = datetime.datetime.now()
    # datade=DO_decry(sensor_sk, Sid, achievemi)
    # end1 = datetime.datetime.now()
    # print('DO decrypt time', end1 - start1)
    #
    # start1 = datetime.datetime.now()
    # data_re_trans(datade, Dev)
    # end1 = datetime.datetime.now()
    # print('DO retransformation time', end1 - start1)
    # # search(Sid, 1, cloud_store, basetable)
    #
    #



    # Batch_search(k, cloud_store, basetable, sensorID):


    #
    # #存100
    # Batch_base = []
    # Batch_deviation = []
    # Sid = 'F' + str(0) + 'S' + str(1)
    # for eline in range(5000, 5100):
    #     base = str_basearray[eline]
    #     deviation = str_deviationarray[eline]
    #     ###将base和deviation转成字节
    #     b_base = base.encode('utf-8')
    #     b_deviation = deviation.encode('utf-8')
    #     m.append(b_base)
    #     #####sensor加密数据并生成tag
    #     # Sid = 'F' + str(0) + 'S' + str(eline)
    #     Batch_base.append(b_base)
    #     Batch_deviation.append(b_deviation)
    # print('len(Batch_base)', len(Batch_base))
    # Fog_rev = rangesensorenc(Batch_base, Batch_deviation, g, pairing, fog_pk[0], Sid, sensor_sk)
    # cloud_rev_data = dedup(Fog_rev, g, pairing, sk_fog, regis, I_fog, pk_c, 1)
    # print('len(cloud_rev_data)',len(cloud_rev_data))
    # start1 = datetime.datetime.now()
    # cloud_store, basetable, I_cloud, I_fog = cloud_layer_dedu(cloud_rev_data, I_cloud, I_fog, cloud_store, time)
    # end1 = datetime.datetime.now()
    # print('cloud-lelvel deduplication time---1', end1 - start1)
    #
    # # 存40
    # Batch_base = []
    # Batch_deviation = []
    # Sid = 'F' + str(0) + 'S' + str(1)
    # for eline in range(5100, 5200):
    #     base = str_basearray[eline]
    #     deviation = str_deviationarray[eline]
    #     ###将base和deviation转成字节
    #     b_base = base.encode('utf-8')
    #     b_deviation = deviation.encode('utf-8')
    #     m.append(b_base)
    #     #####sensor加密数据并生成tag
    #     # Sid = 'F' + str(0) + 'S' + str(eline)
    #     Batch_base.append(b_base)
    #     Batch_deviation.append(b_deviation)
    # print('len(Batch_base)', len(Batch_base))
    # Fog_rev = rangesensorenc(Batch_base, Batch_deviation, g, pairing, fog_pk[0], Sid, sensor_sk)
    # cloud_rev_data = dedup(Fog_rev, g, pairing, sk_fog, regis, I_fog, pk_c, 1)
    # print('len(cloud_rev_data)', len(cloud_rev_data))
    # start1 = datetime.datetime.now()
    # cloud_store, basetable, I_cloud, I_fog = cloud_layer_dedu(cloud_rev_data, I_cloud, I_fog, cloud_store, time)
    # end1 = datetime.datetime.now()
    # print('cloud-lelvel deduplication time---2', end1 - start1)
    #
    # # 存60
    # Batch_base = []
    # Batch_deviation = []
    # Sid = 'F' + str(0) + 'S' + str(1)
    # for eline in range(5300, 5400):
    #     base = str_basearray[eline]
    #     deviation = str_deviationarray[eline]
    #     ###将base和deviation转成字节
    #     b_base = base.encode('utf-8')
    #     b_deviation = deviation.encode('utf-8')
    #     m.append(b_base)
    #     #####sensor加密数据并生成tag
    #     # Sid = 'F' + str(0) + 'S' + str(eline)
    #     Batch_base.append(b_base)
    #     Batch_deviation.append(b_deviation)
    # print('len(Batch_base)', len(Batch_base))
    # Fog_rev = rangesensorenc(Batch_base, Batch_deviation, g, pairing, fog_pk[0], Sid, sensor_sk)
    # cloud_rev_data = dedup(Fog_rev, g, pairing, sk_fog, regis, I_fog, pk_c, 1)
    # print('len(cloud_rev_data)', len(cloud_rev_data))
    # start1 = datetime.datetime.now()
    # cloud_store, basetable, I_cloud, I_fog = cloud_layer_dedu(cloud_rev_data, I_cloud, I_fog, cloud_store, time)
    # end1 = datetime.datetime.now()
    # print('cloud-lelvel deduplication time---3', end1 - start1)
    #
    # # 存80
    # Batch_base = []
    # Batch_deviation = []
    # Sid = 'F' + str(0) + 'S' + str(1)
    # for eline in range(5400, 5500):
    #     base = str_basearray[eline]
    #     deviation = str_deviationarray[eline]
    #     ###将base和deviation转成字节
    #     b_base = base.encode('utf-8')
    #     b_deviation = deviation.encode('utf-8')
    #     m.append(b_base)
    #     #####sensor加密数据并生成tag
    #     # Sid = 'F' + str(0) + 'S' + str(eline)
    #     Batch_base.append(b_base)
    #     Batch_deviation.append(b_deviation)
    # print('len(Batch_base)', len(Batch_base))
    # Fog_rev = rangesensorenc(Batch_base, Batch_deviation, g, pairing, fog_pk[0], Sid, sensor_sk)
    # cloud_rev_data = dedup(Fog_rev, g, pairing, sk_fog, regis, I_fog, pk_c, 1)
    # print('len(cloud_rev_data)', len(cloud_rev_data))
    # start1 = datetime.datetime.now()
    # cloud_store, basetable, I_cloud, I_fog = cloud_layer_dedu(cloud_rev_data, I_cloud, I_fog, cloud_store, time)
    # end1 = datetime.datetime.now()
    # print('cloud-lelvel deduplication time---4', end1 - start1)
    #
    # # 存100
    # Batch_base = []
    # Batch_deviation = []
    # Sid = 'F' + str(0) + 'S' + str(1)
    # for eline in range(5500, 5600):
    #     base = str_basearray[eline]
    #     deviation = str_deviationarray[eline]
    #     ###将base和deviation转成字节
    #     b_base = base.encode('utf-8')
    #     b_deviation = deviation.encode('utf-8')
    #     m.append(b_base)
    #     #####sensor加密数据并生成tag
    #     # Sid = 'F' + str(0) + 'S' + str(eline)
    #     Batch_base.append(b_base)
    #     Batch_deviation.append(b_deviation)
    # print('len(Batch_base)', len(Batch_base))
    # Fog_rev = rangesensorenc(Batch_base, Batch_deviation, g, pairing, fog_pk[0], Sid, sensor_sk)
    # cloud_rev_data = dedup(Fog_rev, g, pairing, sk_fog, regis, I_fog, pk_c, 1)
    # print('len(cloud_rev_data)', len(cloud_rev_data))
    # start1 = datetime.datetime.now()
    # cloud_store, basetable, I_cloud, I_fog = cloud_layer_dedu(cloud_rev_data, I_cloud, I_fog, cloud_store, time)
    # end1 = datetime.datetime.now()
    # print('cloud-lelvel deduplication time---5', end1 - start1)
    #
    #
    #







