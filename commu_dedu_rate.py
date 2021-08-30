
# import os
import matplotlib.pyplot as plt
import numpy as np

# x1 = ["1000", "2000", "3000", "4000",'5000'];
x1 = ["0", "0.2",'0.4','0.6','0.8','1'];






y1 = [1.9450645446813035, 1.5812377929716515, 1.2174110412619996, 0.8535842895523476, 0.48975753784269555, 0.1259307861330436];
y2=[1.9569854736364036, 1.6289215087920514, 1.3008575439476995,0.9727935791033475, 0.6447296142589956, 0.3166656494146436]
# y2 = [1.9569854736364036, 1.6050796508818514, 1.2531738281272995, 0.9012680053727475, 0.5493621826181956, 0.19745635986364357];
y3 = [2.7199249267628036, 2.2011260986368515, 1.6823272705108996, 1.1635284423849475, 0.6447296142589956, 0.1259307861330436];
y4=[2.7199249267628036, 2.2392730712931717, 1.7586212158235395, 1.2779693603539075, 0.7973175048842756, 0.3166656494146436]
# y4=[2.7199249267628036, 2.2154312133829714, 1.7109375000031395, 1.2064437866233075, 0.7019500732434756, 0.19745635986364357]
# y5=[1.4066696167018, 1.68800354004216, 1.96933746338252, 2.25067138672288, 2.53200531006324, 2.8133392334036]
# y6=[1.3685226440454799, 1.6422271728545759,1.9159317016636719,2.189636230472768, 2.463340759281864, 2.7370452880909597]
# 设置输出的图片大小
figsize = 7, 6
figure, ax = plt.subplots(figsize=figsize)
plt.grid(linestyle=":",color="k")
# 在同一幅图片上画两条折线
A,= plt.plot(x1, y1, '*-r', label='DB1 - $l_d$=40', linewidth=3.0, alpha=0.7,markersize=15)
B,= plt.plot(x1, y2, "^-b", label='DB2 - $l_d$=40', linewidth=3, alpha=0.7,markersize=15)
C,= plt.plot(x1, y3, '*--r', label='DB1 - $l_d$=200', linewidth=3, alpha=0.7,markersize=15)
D,= plt.plot(x1, y4, '^--b', label='DB2 - $l_d$=200', linewidth=3, alpha=0.7,markersize=15)
# E,= plt.plot(x1, y5, "^--b", label='Xue et al\'s scheme - DB2', linewidth=3, alpha=0.7,markersize=15)
# F,= plt.plot(x1, y6, 'o--y', label='Shin et al\'s scheme - DB2', linewidth=3, alpha=0.7,markersize=15)
# 设置图例并且设置图例的字体及大小
font1 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 16,
         }
# 设置坐标刻度值的大小以及刻度值的字体
plt.tick_params(labelsize=20)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
font2 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 20,
         }
plt.xlabel('Deduplication rate', font2)
plt.ylabel('Communicaiton Overhead (MB)', font2)
plt.ylim((0,3))
# B,= plt.plot(x1, y2, "^-b", label='Data encryption-dataset1', linewidth=3, alpha=0.7,markersize=15)
# E,=plt.plot(x1, y5, "^-b", label='Data encryption-dataset1', linewidth=3, alpha=0.7,markersize=15)

legend = plt.legend(handles=[A,B,C,D], prop=font1, loc='upper right',ncol=1)

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





plt.savefig('./Communi_dedu_rate.pdf')
plt.show()





