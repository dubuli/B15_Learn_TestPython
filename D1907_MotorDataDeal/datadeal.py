
import copy
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib import pyplot as plot #用来绘制图形
from mpl_toolkits.mplot3d import Axes3D  #用来给出三维坐标系。

with open("data.txt", "r") as f:
    read_raw = f.readlines()

BeginReadMaxTorq = 0                # wait for read
index_line = -1
data_maxtorqTmp = [[0 for i in range(1)] for i in range(100)]
index_maxtorq = -1

for line in read_raw:
    index_line = index_line + 1
    if "gMotorMaxTorque" in line:
        BeginReadMaxTorq = 1        # read begin
    if BeginReadMaxTorq == 1:
        if ";" in line:
            BeginReadMaxTorq = 2    # read over 
        if ("{" in line) and ("}" in line):
            index_maxtorq = index_maxtorq + 1
            tmp = list(map(int, re.findall(r"-?\d+\.?\d*", line)))
            data_maxtorqTmp[index_maxtorq] = tmp
    
    num_maxtorqrows = index_maxtorq + 1
    num_maxtorqcolumns = int((len(data_maxtorqTmp[0]) - 1) / 2)

    data_maxtorq = [[0 for i in range(num_maxtorqcolumns)] for i in range(num_maxtorqrows)]
    for i in range(num_maxtorqrows):
        data_maxtorq[i] = data_maxtorqTmp[i][-num_maxtorqcolumns:]


# plt.plot(data_maxtorq)

figure = plt.figure()
#画出三维坐标系：
axes = Axes3D(figure)
X = np.arange(0, num_maxtorqcolumns, 1)
Y = np.arange(0, num_maxtorqrows, 1)
#限定图形的样式是网格线的样式：
XX, YY = np.meshgrid(X, Y)
ZZ = np.array(data_maxtorq)
#ZZ = 3*(X)**2 + 2*(Y)**2 + 5
#绘制曲面，采用彩虹色着色：
axes.plot_surface(XX, YY, ZZ,cmap='rainbow')
axes.plot_wireframe(XX, YY, ZZ,cmap='rainbow')
plt.show()


pass


