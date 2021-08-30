
# import os
import matplotlib.pyplot as plt
import numpy as np
# Z=np.array([[0.575430,1.123995, 1.677487, 2.269932, 2.818494],
#    [1.194806, 2.353708, 3.528568, 4.663505,5.709708],
#    [1.838058, 3.600404, 5.405579, 7.275809, 9.224342],
#    [2.541207, 5.005619, 7.543864, 10.075068, 13.003269],
#    [3.254329, 6.348031, 9.593327, 12.834788, 16.148864]])
# Z2=np.array([[1.226721, 2.350716, 3.554530, 4.650540, 5.927158],
#    [2.471393, 4.865993, 7.201748, 9.820836, 12.116612],
#    [3.767930, 7.412262, 11.175201, 14.531152, 18.419763],
#    [5.205086, 10.136936, 15.230362, 20.235789, 25.656417],
#    [6.794865, 13.070153, 20.167793,25.971958,33.109522]])
# x1 = ["1000", "2000", "3000", "4000",'5000'];
x1 = ["100", "200", "300", "400",'500'];
# y1 = [0.575430, 1.194806, 1.838058,2.541207,3.254329];
y2 = [1.123995, 2.353708, 3.600404, 5.005619, 6.348031];
y3 = [2.818494, 5.709708, 9.224342, 13.003269, 16.148864];
# y4=[1.226721, 2.471393, 3.767930, 5.205086, 6.794865]
y5=[2.350716, 4.865993, 7.412262, 10.136936, 13.070153]
y6=[5.927158, 12.116612, 18.419763, 25.656417, 33.109522]
# 设置输出的图片大小
figsize = 7, 6
figure, ax = plt.subplots(figsize=figsize)
plt.grid(linestyle=":",color="k")
# 在同一幅图片上画两条折线


# A,= plt.plot(x1, y1, '*-r', label='DB1 - 20', linewidth=3.0, alpha=0.7,markersize=15)
B,= plt.plot(x1, y2, "*-r", label='DB1 - $l_d$=40', linewidth=3, alpha=0.7,markersize=15)
C,= plt.plot(x1, y3, '^-b', label='DB2 - $l_d$=40', linewidth=3, alpha=0.7,markersize=15)
# D,= plt.plot(x1, y4, '*--r', label='DB2 - 20', linewidth=3, alpha=0.7,markersize=15)
E,= plt.plot(x1, y5, "*--r", label='DB1 - $l_d$=100', linewidth=3, alpha=0.7,markersize=15)
F,= plt.plot(x1, y6, '^--b', label='DB2 - $l_d$=100', linewidth=3, alpha=0.7,markersize=15)
# 设置图例并且设置图例的字体及大小
font1 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 19,
         }
# 设置坐标刻度值的大小以及刻度值的字体
plt.tick_params(labelsize=20)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
font2 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 20,
         }
plt.xlabel('Number of training data', font2)
plt.ylabel('Computational Overhead (s) ', font2)
plt.ylim((0, 35))
# B,= plt.plot(x1, y2, "^-b", label='Data encryption-dataset1', linewidth=3, alpha=0.7,markersize=15)
# E,=plt.plot(x1, y5, "^-b", label='Data encryption-dataset1', linewidth=3, alpha=0.7,markersize=15)

legend = plt.legend(handles=[B,C,E,F], prop=font1, loc='upper left',ncol=1)

#
# plt.axes([0.6, 0.2, 0.25, 0.25])  #使用plt.axes
# plt.ylim((0, 0.02))
# legend1 = plt.legend(handles=[B,E], prop=font1, loc='upper right',ncol=1)
# plt.plot()




# 设置横纵坐标的名称以及对应字体格式

# 将文件保存至文件中并且画出图
# plt.savefig('figure.eps')
#
# fig = plt.figure()
# left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
# ax1 = fig.add_axes([left, bottom, width, height])  # main axes
# B=ax1.plot(x1, y2, "^-b", label='Data encryption-dataset1', linewidth=3, alpha=0.7,markersize=15)
# E=ax1.plot(x1, y5, "^-b", label='Data encryption-dataset1', linewidth=3, alpha=0.7,markersize=15)





plt.savefig('./Permu_mix.pdf')
plt.show()





