
# import os
import matplotlib.pyplot as plt
import numpy as np



f, ax = plt.subplots(figsize = (7, 6))
x = np.arange(5)
plt.grid(linestyle=":",color="k")
#client
# y = [0.082, 0.0845, 0.0879, 0.089, 0.091]
#server
y1 = [3090015, 3728400, 4978222, 6004577, 8587243]
#blockchain
# y2 = [0.39, 0.778, 1.558, 3.114, 6.23]
bar_width = 0.25

font1 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 20}
plt.tick_params(labelsize=20)
tick_label = ["100", "200", "400", "800", "1600"]
A=plt.bar(x, y1, bar_width, align="center", color="r", label="Upload on-chain digests", alpha=0.7)
# B=plt.bar(x+bar_width, y2, bar_width,  align="center",color="b", label="Server-side indexes", alpha=0.7)
# C=plt.bar(x+2*bar_width, y2, bar_width,  align="center", color="y",label="Server-side indexes", alpha=0.7)
legend = plt.legend(handles=[A], prop=font1)


font2 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 20}
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
plt.xlabel("Number of keywords",font2)
plt.ylabel("Gas cost", font2)
plt.ylim(3000000,12000000)
plt.yscale('linear')
plt.xticks(x, tick_label)

# plt.legend()
plt.savefig('Gas_cost_Yu.pdf')
plt.show()

# , alpha=0.5






