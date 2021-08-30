import math
import numpy as np
import sys
import operator
import pickle
import copy

#######读deviation和data




f_indextodelete = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/index_to_delete_dataset2.txt', mode = 'rb')
index_to_delete=pickle.load(f_indextodelete)

f_k_test = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/k_test_dataset2.txt', mode = 'rb')
k_test=pickle.load(f_k_test)

print('index_to_delete',index_to_delete)
print('k_test',k_test)

# def Transform(origarray,index_to_delete):
#     basearray=[]
#     deviationarray=[]
#     for list_given in origarray:
#         base=[]
#         deviation=[]
#         for j in range(0,len(list_given)):
#             if j in index_to_delete:
#                 deviation.append(list_given[j])
#             else:
#                 base.append(list_given[j])
#         basearray.append(base)
#         deviationarray.append(deviation)
#     return basearray,deviationarray

def Transform(origarray,index_to_delete):
    str_basearray=[]
    str_deviationarray=[]
    for list_given in origarray:
        str_base = ''
        str_deviation=''
        for j in range(0,len(list_given)):
            if j in index_to_delete:
                str_deviation=str_deviation+str(list_given[j])
            else:
                str_base=str_base+str(list_given[j])
        str_basearray.append(str_base)
        str_deviationarray.append(str_deviation)
    return str_basearray,str_deviationarray

###############判断test set情况
number_chunk=len(k_test)
print('number_chunk',number_chunk)
print('len(k_test[0]',len(k_test[0]))
testdata=k_test.tolist()
str_basearray,str_deviationarray=Transform(testdata,index_to_delete)

f_str_basearray = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/str_basearray_dataset2.txt', mode = 'wb')
pickle.dump(str_basearray,f_str_basearray)
f_str_basearray.close()
f_str_deviationarray = open('/Users/chen/PycharmProjects/ICC_2020_forward secure_verifiable/str_deviationarray_dataset2.txt', mode = 'wb')
pickle.dump(str_deviationarray,f_str_deviationarray)
f_str_deviationarray.close()

