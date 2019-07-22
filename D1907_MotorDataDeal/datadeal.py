import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import copy
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib import pyplot as plot #用来绘制图形
from mpl_toolkits.mplot3d import Axes3D  #用来给出三维坐标系。
import threading  
import time  

# 定义Application类表示应用/窗口，继承Frame类
class Application:
    # Application构造函数，master为窗口的父控件
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("APP")
        self.window.geometry("640x400+100+100")
        self.window.resizable(True, True)

        self.notebook = ttk.Notebook(self.window, width=300, height=300)
        self.notebook.pack(side=tk.LEFT, expand=1, fill="both")
        self.tab1 = tk.Frame(self.window)
        self.notebook.add(self.tab1, text = 'tab1')
        self.tab2 = tk.Frame(self.window)
        self.notebook.add(self.tab2, text = 'tab2')

        self.btn2 = Button(self.tab1, text="datadeal", command=self.__datadealthread)
        self.btn2.pack()

        self.window.mainloop()
    
    def __datadealthread(self):
        th=threading.Thread(target=self.__datadeal,args=())  
        th.setDaemon(True)#守护线程  
        th.start()  
    def __datadeal(self):

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
        # wireframe
        axes.plot_wireframe(XX, YY, ZZ,cmap='rainbow')
        # z contour
        axes.contour(XX, YY, ZZ, zdir = 'z', offset = -2, cmap = plt.get_cmap('rainbow'))
        
        plt.show()
 
# 创建一个Application对象app
app = Application()

