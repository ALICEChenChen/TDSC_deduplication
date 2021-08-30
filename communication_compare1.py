
# import os
import matplotlib.pyplot as plt
import numpy as np

# x1 = ["1000", "2000", "3000", "4000",'5000'];
x1 = ["5000", "6000",'7000','8000','9000','10000'];






y1 = [0.6115422248851554, 0.7124924659742078,0.7876329422011523, 0.8778481483475581, 0.9895334243792572, 1.0728964805622714];
y2 = [1.0251998901386, 1.23023986816632, 1.43527984619404, 1.64031982422176, 1.84535980224948, 2.0503997802772];
y3 = [0.98705291748228, 1.1844635009787359, 1.381874084475192,1.579284667971648, 1.776695251468104, 1.97410583496456];
y4=[1.0530490875263463, 1.2946968078637038, 1.6007547378569413, 1.797178268435915, 2.0872478485145725, 2.2859554290813433]
y5=[1.4066696167018, 1.68800354004216, 1.96933746338252, 2.25067138672288, 2.53200531006324, 2.8133392334036]
y6=[1.3685226440454799, 1.6422271728545759,1.9159317016636719,2.189636230472768, 2.463340759281864, 2.7370452880909597]
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
plt.ylabel('Communicaiton Overhead (MB)', font2)
plt.ylim((0,4.5))
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





plt.savefig('./Communi_compare.pdf')
plt.show()





