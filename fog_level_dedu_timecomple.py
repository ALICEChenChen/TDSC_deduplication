
# import os
import matplotlib.pyplot as plt
import numpy as np

# x1 = ["1000", "2000", "3000", "4000",'5000'];
x1 = ["5000", "6000",'7000','8000','9000','10000'];






y1 = [0.1731662750247318,0.2023715972904104, 0.22489547729533454,0.25132179260300025, 0.28330612182669174,0.30795860290583854];
y2 =[2.24590301514084, 2.695083618169008, 3.144264221197176, 3.593444824225344, 4.042625427253512, 4.49180603028168];
y3 =[3.44038009644186, 4.1284561157302315, 4.816532135018604, 5.504608154306976, 6.192684173595348, 6.88076019288372]
y4= [0.5950107574473809, 0.729694366456417, 0.8965158462540865, 1.008634567262593, 1.1674785614035095, 1.2807369232201236];
y5=[2.62737274170404, 3.152847290044848, 3.678321838385656, 4.203796386726464, 4.729270935067272, 5.25474548340808]
y6=[3.82184982300506, 4.586219787606072, 5.3505897522070835, 6.114959716808096, 6.879329681409108, 7.64369964601012]
# 设置输出的图片大小
figsize = 7, 6
figure, ax = plt.subplots(figsize=figsize)
plt.grid(linestyle=":",color="k")
# 在同一幅图片上画两条折线
A,= plt.plot(x1, y1, '*-r', label='Our scheme - DB1', linewidth=3.0, alpha=0.7,markersize=15)
B,= plt.plot(x1, y2, "^-b", label='Xue et al\'s scheme - DB1', linewidth=3, alpha=0.7,markersize=15)
C,= plt.plot(x1, y3, 'o-y', label='Shin et al\'s scheme - DB1', linewidth=3, alpha=0.7,markersize=15)
D,= plt.plot(x1, y4, '*--r', label='Our scheme - DB2', linewidth=3, alpha=0.7,markersize=15)
E,= plt.plot(x1, y5, "^--b", label='Xue et al\'s scheme - DB2', linewidth=3, alpha=0.7,markersize=15)
F,= plt.plot(x1, y6, 'o--y', label='Shin et al\'s scheme - DB2', linewidth=3, alpha=0.7,markersize=15)
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
plt.xlabel('Number of data', font2)
plt.ylabel('Storage Overhead (MB)', font2)
plt.ylim((0,12))
# B,= plt.plot(x1, y2, "^-b", label='Data encryption-dataset1', linewidth=3, alpha=0.7,markersize=15)
# E,=plt.plot(x1, y5, "^-b", label='Data encryption-dataset1', linewidth=3, alpha=0.7,markersize=15)

legend = plt.legend(handles=[A,B,C,D,E,F], prop=font1, loc='upper left',ncol=1)

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





plt.savefig('./torage_compare.pdf')
plt.show()





