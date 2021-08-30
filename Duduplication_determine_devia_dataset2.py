import math
import numpy as np
import sys
import operator
import datetime
import pickle
import copy
txt = []
with open('./DB2_1.txt','r',  encoding='UTF-8') as f:
    for line in f.readlines():
        sen = line.strip('\n').split(',')
        l = []
        for s in sen:
            s = s.strip()
            l.append(s)
        txt.append(l)
# change into the same length.
with open('./DB2_2.txt','r',  encoding='UTF-8') as f:
    for line in f.readlines():
        sen = line.strip('\n').split(',')
        l = []
        for s in sen:
            s = s.strip()
            l.append(s)
        txt.append(l)
new=[]
leneachitem=[5, 6, 40, 2, 9, 10, 4, 4, 8, 8, 5, 50]
for line in txt:
    if len(line)==12:
        eachline=''
        newline = []
        for i in range(0, len(line)):
            tt=' ' * (leneachitem[i] - len(line[i])) + line[i]
            newline.append(tt)
            eachline += tt
        new.append(eachline)

# change string into binary int
new1=np.array(new)
tt=[]
for t in new:
    c=(" ".join(f"{ord(i):08b}" for i in t))
    teachline=[]
    for i in c:
        if i!=' ':
            teachline.append(int(i))
    if len(teachline)==1208:
        mk=np.array(teachline)
        tt.append(mk)
# print('len(tt)',len(tt))
m=[]
DATA_num=500
kk=0
m_test=[]
for i in tt:
    mm=[]
    qq=[]
    kk=kk+1
    if kk<=DATA_num:
        for j in i:
            mm.append(j)
        tk=np.array(mm)
        m.append(tk)
    else:
        for j in i:
            qq.append(j)
        qk=np.array(qq)
        m_test.append(qk)
# print('m',type(m))
# print('m',type(m[0]))
# print('len(m)',len(m))
###########k是前100行数据
k=np.array(m)
k_test=np.array(m_test)
listsame=[]
listdif=[]
u=[]
o=0
start1=datetime.datetime.now()
#label the item whose item all the same
for item in range(0,len(k[0])):
    f=(k[:,item])
    w=sum(f)
    r=np.transpose(f).reshape((len(f),1))
    if w==0 or w==DATA_num:
        listsame.append(item)
    else:
        if o==0:
            mathecheng=r
            o=o+1
        else:
            mathecheng=np.hstack((mathecheng,r))
        listdif.append(item)
# print('mathecheng',mathecheng)
# print(len(mathecheng))
# print(len(listdif))
# print(listsame)
# print(len(listsame))
# print('listdif',listdif)

np.set_printoptions(threshold=np.inf)

################计算pearson系数##############

# print('len(mathecheng)1',len(mathecheng))

start1=datetime.datetime.now()
pearson=np.corrcoef(mathecheng, rowvar=False)

# sys.stdout = open('recode.log', mode = 'w',encoding='utf-8')
###############delete dialog element (equal 1)
pearson=pearson.tolist()
for i in range(0, len(pearson)):
    pearson[i].pop(i)

peardic={}
for i in range(0,len(pearson)):
    linemax = max(map(abs, pearson[i]))
    linekey = listdif[i]
    peardic[linekey]=linemax

######################peardic 根据值从大到小排序
# d_order=sorted(peardic.items(),key=lambda x:x[1],reverse=True)
d_order=sorted(peardic.items(),key=lambda x:x[1],reverse=False)
def storage(origarray,index_to_delete):
    newarray=[]
    for list_given in origarray:
        index_to_delete.sort(reverse=True)
        for index in (index_to_delete):
            list_given.pop(index)
        newarray.append(list_given)
    # print('len(newarray[0])', len(newarray[0]))
    size_b=len(newarray[0])
    size_d=len(index_to_delete)
    number_chunk=len(origarray)
    basenum=number_chunk
    listnot=[]
    for i in range(0,len(newarray)):
        for j in range(i+1,len(newarray)):
            if j not in listnot:
                if (operator.eq(newarray[i],newarray[j])):
                    listnot.append(j)
                    basenum=basenum-1
    ##########total storage space
    totalstorage=basenum*size_b+number_chunk*(math.ceil(math.log(basenum,2)) + size_d)
    # print('basenum', basenum)
    # print('size_b', size_b)
    # print('number_chunk', number_chunk)
    # print('size_d', size_d)
    # print('totalstorage----------------',totalstorage)
    return totalstorage


###################计算存储空间
origa=k.tolist()
# print('len(origa)',len(origa))
# origa=m.tolist()
ori=copy.deepcopy(origa)
index_to_delete = []
S = storage(ori, index_to_delete)
d_list=[]
for i in range(0,len(d_order)):
    d_list.append(d_order[i][0])
index_to_delete.append(d_list[0])
ori=copy.deepcopy(origa)
S_1 = storage(ori, index_to_delete)
l_d=1
# print('S',S)
# print('S_1',S_1)
end2=datetime.datetime.now()
while(l_d<320):
    index_to_delete.append(d_list[l_d])
    S=S_1
    ori = copy.deepcopy(origa)
    # print('len(ori[0])?????', len(ori[0]))
    S_1=storage(ori, index_to_delete)
    l_d=l_d+1


end1=datetime.datetime.now()
print('permutation set determination time',end1-start1)
# print(index_to_delete)
# print('before iteration time',end2-start1)

f_indextodelete = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/index_to_delete_dataset2.txt', mode = 'wb')
pickle.dump(index_to_delete,f_indextodelete)
f_indextodelete.close()
f_k_test = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/k_test_dataset2.txt', mode = 'wb')
pickle.dump(k_test,f_k_test)
f_k_test.close()




# ###############判断test set情况
# number_chunk=len(k_test)
# testdata=k_test.tolist()
# test_ori=copy.deepcopy(testdata)
# ########storage with generalized deduplication
# totalstorage=storage(test_ori,index_to_delete)
# print('totalstorage with GD',totalstorage)
# ########storage with classical deduplication
# chunknum=number_chunk
# listnot = []
# for i in range(0, len(k_test)):
#     for j in range(i + 1, len(k_test)):
#         if j not in listnot:
#             if all(k_test[i]==k_test[j]):
#             # (operator.eq(k_test[i], k_test[j])):
#                 listnot.append(j)
#                 chunknum = chunknum - 1
# print('storage with classical deduplication', chunknum * len(k_test[0]))
# print('storage without deduplication',number_chunk*len(k_test[0]))
#


