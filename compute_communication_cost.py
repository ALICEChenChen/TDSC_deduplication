devia1=360
devia2=320
base1=568-devia1
base2=1208-devia2
totalnum=10000
num_base1=448
num_base2=3128
dedurate=1
# store1=((base1*(1-dedurate)*totalnum)+devia1*totalnum+totalnum+totalnum*16)*0.000000119209289551
# store2=((base2*(1-dedurate)*totalnum)+devia2*totalnum+totalnum+totalnum*16)*0.000000119209289551
store1=((base1*num_base1)+devia1*totalnum+totalnum*16)*0.000000119209289551
store2=((base2*num_base2)+devia2*totalnum+totalnum*16)*0.000000119209289551



print('store1',store1)
print('store2',store2)

def our_com_rate(N_data,rate,l_b,l_d):
    N_base=N_data*rate
    commu = ((32 + l_d + 16 + 16) * (N_data - N_base) + (32 + l_b + l_d + 16 + 1024) * N_base + 1024 * 16) * 0.000000119209289551
    print(N_data, 'our storage:', commu)


# our_com_rate(10000, 0,518,40)
# our_com_rate(10000, 0.2,518,40)
# our_com_rate(10000, 0.4,518,40)
# our_com_rate(10000, 0.6,518,40)
# our_com_rate(10000, 0.8,518,40)
# our_com_rate(10000, 1,518,40)
#
#
our_com_rate(10000, 0,368,200)
our_com_rate(10000, 0.2,368,200)
our_com_rate(10000, 0.4,368,200)
our_com_rate(10000, 0.6,368,200)
our_com_rate(10000, 0.8,368,200)
our_com_rate(10000, 1,368,200)


# our_com_rate(10000, 0,1168,40)
# our_com_rate(10000, 0.2,1168,40)
# our_com_rate(10000, 0.4,1168,40)
# our_com_rate(10000, 0.6,1168,40)
# our_com_rate(10000, 0.8,1168,40)
# our_com_rate(10000, 1,1168,40)


our_com_rate(10000, 0,1008,200)
our_com_rate(10000, 0.2,1008,200)
our_com_rate(10000, 0.4,1008,200)
our_com_rate(10000, 0.6,1008,200)
our_com_rate(10000, 0.8,1008,200)
our_com_rate(10000, 1,1008,200)



def our_commu(N_data,  N_base,l_b,l_d):
    commu=((32+l_d+16+16)* (N_data-N_base)+(32+l_b+l_d+16+1024)*N_base+1024*16) *0.000000119209289551
    print(N_data,'our storage:',commu )

#
#
# our_commu(5000, 1719,908,300)
# our_commu(6000, 1971,908,300)
# our_commu(7000, 2110,908,300)
# our_commu(8000, 2315,908,300)
# our_commu(9000, 2614,908,300)
# our_commu(10000, 2789,908,300)
#
#
#
# our_commu(5000, 3652,908,300)
# our_commu(6000, 4520,908,300)
# our_commu(7000, 5670,908,300)
# our_commu(8000, 6340,908,300)
# our_commu(9000, 7420,908,300)
# our_commu(10000, 8100,908,300)
#
def shin_method(N_data, l_data):
    commu = (64 +1024 + l_data) * N_data * 0.000000119209289551
    print(N_data, 'shin_method::', commu)
#
def xue_method(N_data,l_data):
    commu=(1024+128+l_data)*N_data*0.000000119209289551
    print(N_data, 'xue_method::', commu)
#
# shin_method(5000, 568)
# shin_method(6000, 568)
# shin_method(7000, 568)
# shin_method(8000, 568)
# shin_method(9000, 568)
# shin_method(10000, 568)
#
# shin_method(5000, 1208)
# shin_method(6000, 1208)
# shin_method(7000, 1208)
# shin_method(8000, 1208)
# shin_method(9000, 1208)
# shin_method(10000, 1208)
#
# xue_method(5000, 568)
# xue_method(6000, 568)
# xue_method(7000, 568)
# xue_method(8000, 568)
# xue_method(9000, 568)
# xue_method(10000, 568)
#
# xue_method(5000, 1208)
# xue_method(6000, 1208)
# xue_method(7000, 1208)
# xue_method(8000, 1208)
# xue_method(9000, 1208)
# xue_method(10000, 1208)