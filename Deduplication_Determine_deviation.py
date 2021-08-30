import math
import numpy as np
import sys
import operator
import pickle
import copy
txt = []
with open('./climat_data_200805.txt','r',  encoding='UTF-8') as f:
    for line in f.readlines():
        # sen = line.strip('\n').split('  ')
        sen = line.strip('\n')
        # print(len(sen))
        txt.append(sen)
print(txt)
print(type(txt[0]))

with open('./climat_data_201106.txt','r',  encoding='UTF-8') as f:
    for line in f.readlines():
        # sen = line.strip('\n').split('  ')
        sen = line.strip('\n')
        # print(len(sen))
        txt.append(sen)

with open('./climat_data_201306.txt','r',  encoding='UTF-8') as f:
    for line in f.readlines():
        # sen = line.strip('\n').split('  ')
        sen = line.strip('\n')
        # print(len(sen))
        txt.append(sen)

with open('./climat_data_201307.txt','r',  encoding='UTF-8') as f:
    for line in f.readlines():
        # sen = line.strip('\n').split('  ')
        sen = line.strip('\n')
        # print(len(sen))
        txt.append(sen)

with open('./climat_data_201308.txt','r',  encoding='UTF-8') as f:
    for line in f.readlines():
        # sen = line.strip('\n').split('  ')
        sen = line.strip('\n')
        # print(len(sen))
        txt.append(sen)
# # change into the same length.
new=[]
for line in txt:
    eachline = ''
    eachline=line[5:7]+line[12:15]+line[17:23]+line[25:31]+line[32:38]+line[39:45]+line[46:52]+line[55:61]+line[64:70]+line[73:79]+line[81:87]+line[89:95]+line[97:103]
    new.append(eachline)
print(len(new))
print(new[70])



# new=[]
# leneachitem=[5, 6, 40, 2, 9, 10, 4, 4, 8, 8, 5, 50]
# for line in txt:
#     if len(line)==12:
#         eachline=''
#         newline = []
#         for i in range(0, len(line)):
#             tt=' ' * (leneachitem[i] - len(line[i])) + line[i]
#             newline.append(tt)
#             eachline += tt
#     new.append(eachline)

# change string into binary int
new1=np.array(new)
tt=[]
for t in new:
    c = (" ".join(f"{ord(i):08b}" for i in t))
    # print(c)
    teachline = []
    for i in c:
        if i != ' ':
            teachline.append(int(i))
    mk = np.array(teachline)
    tt.append(mk)
print('len(tt)',len(tt))
print(tt[0])
m=[]
kk=0
m_test=[]
for i in tt:
    mm=[]
    qq=[]
    kk=kk+1
    if kk<=100:
        for j in i:
            mm.append(j)
        tk=np.array(mm)
        m.append(tk)
    else:
        for j in i:
            qq.append(j)
        qk=np.array(qq)
        m_test.append(qk)
print('m',type(m))
print('m',type(m[0]))
print('len(m)',len(m))
###########k是前100行数据
k=np.array(m)
k_test=np.array(m_test)
# f=open("C:\\Users\\czhang455\\PycharmProjects\\fog_cloud\\data.txt",'w')
# pickle.dump(k,f)
listsame=[]
listdif=[]
u=[]
o=0
#label the item whose item all the same
for item in range(0,len(k[0])):
    f=(k[:,item])
    w=sum(f)
    r=np.transpose(f).reshape((len(f),1))
    if w==0 or w==100:
        listsame.append(item)
    else:
        if o==0:
            mathecheng=r
            o=o+1
        else:
            mathecheng=np.hstack((mathecheng,r))
        listdif.append(item)
print('mathecheng',mathecheng)
print(len(listdif))
print(listsame)
print(len(listsame))
print('listdif',listdif)

np.set_printoptions(threshold=np.inf)

################计算pearson系数##############
pearson=np.corrcoef(mathecheng, rowvar=False)
# sys.stdout = open('recode.log', mode = 'w',encoding='utf-8')
# print('pearson',pearson)
# print('pearson[0]', pearson[0])

###############delete dialog element (equal 1)
pearson=pearson.tolist()
for i in range(0, len(pearson)):
    pearson[i].pop(i)

peardic={}
for i in range(0,len(pearson)):
    linemax = max(map(abs, pearson[i]))
    linekey = listdif[i]
    peardic[linekey]=linemax
# print('peardic',peardic)
# print(len(peardic))

######################peardic 根据值从大到小排序
# d_order=sorted(peardic.items(),key=lambda x:x[1],reverse=True)
d_order=sorted(peardic.items(),key=lambda x:x[1],reverse=False)
# print('d_order',d_order)
# print('type(d_order)',type(d_order))
# print('(d_order[0])',(d_order[0]))
# print('type(d_order[0])',type(d_order[0]))


def storage(origarray,index_to_delete):
    newarray=[]
    for list_given in origarray:
        index_to_delete.sort(reverse=True)
        for index in (index_to_delete):
            list_given.pop(index)
        newarray.append(list_given)
    print('newarray[0]',newarray[0])
    print(type(newarray[0]))
    print('len(newarray[0])', len(newarray[0]))
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
    print('basenum', basenum)
    print('size_b', size_b)
    print('number_chunk', number_chunk)
    print('size_d', size_d)
    print('totalstorage----------------',totalstorage)
    return totalstorage


###################计算存储空间
origa=k.tolist()
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
print('S',S)
print('S_1',S_1)
while(l_d<120):
# while(abs(S-S_1)<11000):
    index_to_delete.append(d_list[l_d])
    S=S_1
    ori = copy.deepcopy(origa)
    print('len(ori[0])?????', len(ori[0]))
    S_1=storage(ori, index_to_delete)
    l_d=l_d+1
    print('S', S)
    print('S_1', S_1)
print(index_to_delete)

f_indextodelete = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/index_to_delete.txt', mode = 'wb')
pickle.dump(index_to_delete,f_indextodelete)
f_indextodelete.close()
f_k_test = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/k_test.txt', mode = 'wb')
pickle.dump(k_test,f_k_test)
f_k_test.close()


