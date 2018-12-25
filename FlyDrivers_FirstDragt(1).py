#==================================================
# Version		0.01
#==================================================

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import copy

global DegComBox
DegComBox = []
global DegClkRowId
DegClkRowId = 0
global DegClkIndex
DegClkIndex = 0
global DegClkColumnId
DegClkColumnId = 0

global OpComBox
OpComBox = []
global OpClkRowId
OpClkRowId = 0
global OpClkIndex
OpClkIndex = 0
global OpClkColumnId
OpClkColumnId = 0

global DegSecList
global OpSecList
global read_raw
global lineindex_time
global filename                                       #载入的文档路弿
global TreeviewPst
global TreeLineNum
global ParList
global DegList
global OpList
global DbClkFished
global Precision
DegSecList = ['保持','0.1','0.01','0.001','0.0001','0.00001','1','End']
Precision =  [1.0,    0.1,  0.01,  0.001,  0.0001,  0.00001,  1.0, ]
OpSecList =  ['无操作','正负转换','取绝对值','End']
DbClkFished = 1
TreeLineNum = 666
TreeviewPst = 0.0
ParList = []
DegList = []
OpList = []

# 选择文件函数，并对Treeview的显示内容进行初始化
def SelectFile():
    global filename
    global TreeLineNum
    global read_raw
    global read_ripe
    global lineindex_time
    global filename
    
    varnum = 0
    InfoLabel.config(text=('Select file...'))
    filename = filedialog.askopenfilename()
    if filename == '':
    	InfoLabel.config(text=('None file selected!'))
    	return
    dir.set(filename)
    # open the csv file
    with open(filename) as f_in:
        # lookup the line index of 时间
        read_raw = f_in.readlines()
        read_ripe = read_raw
        k = 0
        for line in read_raw:
            linelist = line.split(",")
            if linelist[0] == "时间":
                lineindex_time = k      # the line number of the varname 时间/ U2-00/...
                varnum = len(linelist)
                # print(linelist)
                break                   # linelist is the varname 时间/ U2-00/...
            k = k + 1
    # LineNum = 100                                     #此处进行赋值，决定要创建多少行Entry类型文本柿
    i = 0
    
    # 删除原有Treeview里面的所有item，避免第二次选择插入项过多的问题
    if TreeLineNum != 666:
    	TreeIidList = ParTreeview.get_children()
    	for item in TreeIidList:
    	    ParTreeview.delete(item)
    	    DegTreeview.delete(item)
    	    OpTreeview.delete(item)
    
    # 初始化插入Treeview的所有内容，并对tags和idd进行赋值。Tags用于改变底色。idd用于识别
    while i < varnum:
        ParList[i] = linelist[i]
        ParTreeview.insert('',i,values=(ParList[i]),tags='Par'+str(i),iid=str(i))
        DegTreeview.insert('',i,values=(DegList[i]),tags='Deg'+str(i),iid=str(i))
        OpTreeview.insert('',i,values=(OpList[i]),tags='Op'+str(i),iid=str(i))
        i = i + 1
    
    TreeLineNum = varnum
    
    # 对每个Treeview的每个item进行底色设置。
    for index in range(TreeLineNum):
        if(1 == (index % 2)):
            ParTreeview.tag_configure('Par' + str(index),background='#E0EFFF')
        else:
            ParTreeview.tag_configure('Par' + str(index),background='#FFFFFF')

        if(DegList[index] != DegSecList[0]):
            DegTreeview.tag_configure('Deg' + str(index),background='#D869FF')
        elif(1 == (index % 2)):
            DegTreeview.tag_configure('Deg' + str(index),background='#E0EFFF')
        else:
            DegTreeview.tag_configure('Deg' + str(index),background='#FFFFFF')

        if(OpList[index] != OpSecList[0]):
            OpTreeview.tag_configure('Op' + str(index),background='#D869FF')
        elif(1 == (index % 2)):
            OpTreeview.tag_configure('Op' + str(index),background='#E0EFFF')
        else:
            OpTreeview.tag_configure('Op' + str(index),background='#FFFFFF')
    
    InfoLabel.config(text=('Select file finished!'))
    BarSizeAutoSet(0)


# 进行文件转换和写入操作
def ChangeFile():
    global read_raw
    global lineindex_time
    global read_ripe
    global TreeLineNum
    global Precision
    global DegSecList
    global DegList
    global OpList
    
    OperateLineNum = 0

    InfoLabel.config(text=('Start changing file ...'))
    
    read_ripe = copy.copy(read_raw)
    
    for i in range(TreeLineNum):
        if OpList[i] == '正负转换':
            print(i)
            # modify the data
            rowindex = i

            temp = 0
            while 1:
                if(DegSecList[temp] == 'End'):
                    InfoLabel.config(text=('Precision Error!'))
                    return
                elif(DegSecList[temp] == DegList[i]):
                    break
                else:
                    temp = temp +1
            prsition = Precision[temp]
            
            OperateLineNum = OperateLineNum + 1
            
            for index in range(lineindex_time + 1, len(read_raw)):  #read_raw[( + 1):]:
                linelist = read_ripe[index].split(",")
                value = float(linelist[rowindex])
                if value < 0:
                    value = value + 65536 * prsition
                    value = round(value, 3)
                elif value > 32767 * prsition:
                    value = value - 65536 * prsition
                    value = round(value, 3)
                linelist[rowindex] = str(value)
                read_ripe[index] = ','.join(linelist)
            print(i)    
            
            #write the data
        elif OpList[i] == '取绝对值':
            print(i)
            # modify the data
            rowindex = i
            
            OperateLineNum = OperateLineNum + 1
            
            for index in range(lineindex_time + 1, len(read_raw)):  #read_raw[( + 1):]:
                linelist = read_ripe[index].split(",")
                value = float(linelist[rowindex])
                if value < 0:
                    value = - value
                    value = round(value, 3)
                linelist[rowindex] = str(value)
                read_ripe[index] = ','.join(linelist)
            print(i)    
                # print(linelist)
            #write the data
        elif(TreeLineNum == (i - 1)):
            InfoLabel.config(text=('Operation Error!'))
            return
            
    if(0 == OperateLineNum):
        InfoLabel.config(text=('No Operation'))
    else:
        with open(filename + 'change.csv', 'w') as f_out:
            f_out.writelines(read_ripe)
        InfoLabel.config(text=('Operation finished!'))

def DegDbClear(event):
    global TreeLineNum
    DegClkRowId = DegTreeview.identify_row(event.y)
    DegClkColumnId = DegTreeview.identify_column(event.x)
    if(TreeLineNum == 666) or (DegClkRowId != ''):
        return

    for i in range(TreeLineNum):
        DegList[i] = DegSecList[0]
        DegTreeview.set(i ,DegClkColumnId, DegList[i])

        if(DegList[i] != DegSecList[0]):
            DegTreeview.tag_configure('Deg' + str(i),background='#D869FF')
        elif(1 == (i % 2)):
            DegTreeview.tag_configure('Deg' + str(i),background='#E0EFFF')
        else:
            DegTreeview.tag_configure('Deg' + str(i),background='#FFFFFF')

def OpDbClear(event):
    global TreeLineNum
    OpClkRowId = OpTreeview.identify_row(event.y)
    OpClkColumnId = OpTreeview.identify_column(event.x)
    if(TreeLineNum == 666) or (OpClkRowId != ''):
        return

    for i in range(TreeLineNum):
        OpList[i] = OpSecList[0]
        OpTreeview.set(i ,OpClkColumnId, OpList[i])

        if(OpList[i] != OpSecList[0]):
            OpTreeview.tag_configure('Op' + str(i),background='#D869FF')
        elif(1 == (i % 2)):
            OpTreeview.tag_configure('Op' + str(i),background='#E0EFFF')
        else:
            OpTreeview.tag_configure('Op' + str(i),background='#FFFFFF')

# 双击Treeview改变值，有下拉框的版本中，该函数未使用
def DegDBClick(event):
    global TreeLineNum
    global DegList
    global DegSecList
#    item = DegTreeview.selection()[0]
#    index = DegTreeview.index(item)
    item = DegTreeview.identify_row(event.y)
    index = DegTreeview.index(item)
    
    DegIndex = DegSecList.index(DegList[index])
    if('End' == DegSecList[DegIndex + 1]):
        DegList[index] = DegSecList[0]
    else:
        DegList[index] = DegSecList[DegIndex + 1]
        
    DegTreeview.delete(item)
    DegTreeview.insert('',index,values=(DegList[index]),tags='Deg'+str(index),iid=str(index))

    if(DegList[index] != DegSecList[0]):
        DegTreeview.tag_configure('Deg' + str(index),background='#D869FF')
    elif(1 == (index % 2)):
        DegTreeview.tag_configure('Deg' + str(index),background='#E0EFFF')
    else:
        DegTreeview.tag_configure('Deg' + str(index),background='#FFFFFF')

# 双击Treeview改变值，有下拉框的版本中，该函数未使用
def OpDBClick(event):
    global TreeLineNum
    global OpList
    global OpSecList
    item = OpTreeview.identify_row(event.y)
    index = OpTreeview.index(item)
    
    OpIndex = OpSecList.index(OpList[index])
    if('End' == OpSecList[OpIndex + 1]):
        OpList[index] = OpSecList[0]
    else:
        OpList[index] = OpSecList[OpIndex + 1]
        
    OpTreeview.delete(item)
    OpTreeview.insert('',index,values=(OpList[index]),tags='Op'+str(index),iid=str(index))

    if(OpList[index] != OpSecList[0]):
        OpTreeview.tag_configure('Op' + str(index),background='#D869FF')
    elif(1 == (index % 2)):
        OpTreeview.tag_configure('Op' + str(index),background='#E0EFFF')
    else:
        OpTreeview.tag_configure('Op' + str(index),background='#FFFFFF')

# 滑块移动，对应三个Treeview同时进行上下滑动。有三种方式：拉滑块；点击滚动条；点击上下按钮
def BarMove(*Date):
    global TreeviewPst
    global TreeLineNum
    if 666 == TreeLineNum:
        return

    if DegComBox:
        DegComBox.destroy()    
    if OpComBox:
        OpComBox.destroy()

    if(Date[0] == 'moveto'):
        BarPos = float(Date[1])
        if(BarPos > (1.0-TreeviewPst)):
            BarPos = (1.0-TreeviewPst)
        elif(BarPos < 0):
            BarPos = 0
        startP=BarPos
    elif(Date[0] == 'scroll'):
        startP = float((bar.get())[0])
        if(Date[2] == 'pages'):
            if(Date[1] == '1'):
                startP = startP + TreeviewPst
                if(startP > (1.0 - TreeviewPst)):
                    startP = 1.0 - TreeviewPst
            elif(Date[1] == '-1'):
                startP = startP - TreeviewPst
                if(startP < 0.0):
                    startP = 0.0
        elif(Date[2] == 'units'):
            TreeUnit = 1.0 / TreeLineNum
            if(Date[1] == '1'):
                startP = startP + TreeUnit
                if(startP > (1.0 - TreeviewPst)):
                    startP = 1.0 - TreeviewPst
            elif(Date[1] == '-1'):
                startP = startP - TreeUnit
                if(startP < 0.0):
                    startP = 0.0   
    EndP = startP + TreeviewPst
    bar.set(str(startP),str(EndP))
    ParTreeview.yview(MOVETO,startP)
    DegTreeview.yview(MOVETO,startP)
    OpTreeview.yview(MOVETO,startP)

# Paraview的点击事件，对应选中操作，并清除创建的下拉框
def ParClick(event):
    global TreeLineNum
    if(TreeLineNum == 666):
        return
    
    if DegComBox:
        DegComBox.destroy()    
    if OpComBox:
        OpComBox.destroy()
        
    item = ParTreeview.identify_row(event.y)
    index = ParTreeview.index(item)
    DegTreeview.selection_set(item)
    OpTreeview.selection_set(item)
    ParTreeview.selection_set(item)
    
    if(DegList[index] != DegSecList[0]):
        DegTreeview.selection_remove(item)
        
    if(OpList[index] != OpSecList[0]):
        OpTreeview.selection_remove(item)

# 按钮抬起操作，用于右边两个Treeview
def TreeButtonRelease(event):
    global TreeLineNum
    if(TreeLineNum == 666):
        return
        
    item = ParTreeview.identify_row(event.y)
    index = ParTreeview.index(item)
    DegTreeview.selection_set(item)
    OpTreeview.selection_set(item)
    ParTreeview.selection_set(item)
    
    if(DegList[index] != DegSecList[0]):
        DegTreeview.selection_remove(item)
        
    if(OpList[index] != OpSecList[0]):
        OpTreeview.selection_remove(item)
      
# 下拉框选中值之后，对对应的Treeview进行操作，并清除当前的下拉框
def DegComBoxSeclected(*Date):
    global DegClkIndex
    global TreeLineNum
    global DegClkRowId
    global OpList
    
    DegList[DegClkIndex] = DegComBox.get()
    DegComBox.destroy()
    
    DegTreeview.delete(DegClkRowId)
    DegTreeview.insert('',DegClkIndex,values=(DegList[DegClkIndex]),tags='Deg'+str(DegClkIndex),iid=str(DegClkIndex))

    if(DegList[DegClkIndex] != DegSecList[0]):
        DegTreeview.tag_configure('Deg' + str(DegClkIndex),background='#D869FF')
    elif(1 == (DegClkIndex % 2)):
        DegTreeview.tag_configure('Deg' + str(DegClkIndex),background='#E0EFFF')
    else:
        DegTreeview.tag_configure('Deg' + str(DegClkIndex),background='#FFFFFF')

# 精度所在的Treeview的点击操作，创建一个下拉框。
def DegClick(event):
    global DegComBox
    global TreeLineNum
    global DegClkRowId
    global DegClkIndex
    global DegClkColumnId
    if(TreeLineNum == 666):
        return
    
    if DegComBox:
        DegComBox.destroy()    
    if OpComBox:
        OpComBox.destroy()      
    
    DegClkRowId = DegTreeview.identify_row(event.y)
    DegClkColumnId = DegTreeview.identify_column(event.x)
   
    if(DegClkRowId == ''):
       return

    DegClkIndex = ParTreeview.index(DegClkRowId)
    
    x,y,width,height = DegTreeview.bbox(DegClkRowId, DegClkColumnId)
    pady = height // 2
    
    DegComBox = ttk.Combobox(DegTreeview, width=int(width/10))
    DegComBox.config(values = DegSecList)
    DegComBox.current(DegSecList.index(DegList[DegClkIndex]))
    DegComBox.place( x=x, y=y+pady,width=width, anchor=W)
    DegComBox.bind("<<ComboboxSelected>>",DegComBoxSeclected)
    
# 下拉框选中值之后，对对应的Treeview进行操作，并清除当前的下拉框
def OpComBoxSeclected(*Date):
    global OpClkIndex
    global TreeLineNum
    global OpClkRowId
    global OpList
    
    OpList[OpClkIndex] = OpComBox.get()
    OpComBox.destroy()
    
    OpTreeview.delete(OpClkRowId)
    OpTreeview.insert('',OpClkIndex,values=(OpList[OpClkIndex]),tags='Op'+str(OpClkIndex),iid=str(OpClkIndex))

    if(OpList[OpClkIndex] != OpSecList[0]):
        OpTreeview.tag_configure('Op' + str(OpClkIndex),background='#D869FF')
    elif(1 == (OpClkIndex % 2)):
        OpTreeview.tag_configure('Op' + str(OpClkIndex),background='#E0EFFF')
    else:
        OpTreeview.tag_configure('Op' + str(OpClkIndex),background='#FFFFFF')

# Operation所在的Treeview的点击操作，创建一个下拉框。
def OpClick(event):
    global OpComBox
    global TreeLineNum
    global OpClkRowId
    global OpClkIndex
    global OpClkColumnId
    if(TreeLineNum == 666):
        return
    
    if DegComBox:
        DegComBox.destroy()    
    if OpComBox:
        OpComBox.destroy()  
    
    OpClkRowId = OpTreeview.identify_row(event.y)
    OpClkColumnId = OpTreeview.identify_column(event.x)
   
    if(OpClkRowId == ''):
       return

    OpClkIndex = ParTreeview.index(OpClkRowId)
    
    x,y,width,height = OpTreeview.bbox(OpClkRowId, OpClkColumnId)
    pady = height // 2
    
    OpComBox = ttk.Combobox(OpTreeview,width= int(width/10))
    OpComBox.config(values = OpSecList)
    OpComBox.current(OpSecList.index(OpList[OpClkIndex]))
    OpComBox.place( x=x, y=y+pady, width=width, anchor=W)
    OpComBox.bind("<<ComboboxSelected>>",OpComBoxSeclected)

# 根据窗口自动调整滑动条的滑块大小
def BarSizeAutoSet(event):
    global TreeviewPst
    global TreeLineNum
    global DegTreeview
    global DegComBox
    global DegClkRowId
    global DegClkColumnId
    global OpTreeview
    global OpComBox
    global OpClkRowId
    global OpClkColumnId
    
    if(TreeLineNum == 666):
    	return
    
    if(str(event) == '0'):
        win.update()
        TreeHigh = ParTreeview.winfo_height()
    else:
        TreeHigh = event.height
        if DegComBox:
            x,y,width,height = DegTreeview.bbox(DegClkRowId,DegClkColumnId)
            pady = height // 2
            DegComBox.place( x=x, y=y+pady, width=width, anchor=W)
        if OpComBox:
            x,y,width,height = OpTreeview.bbox(OpClkRowId, OpClkColumnId)
            pady = height // 2
            OpComBox.place( x=x, y=y+pady, width=width, anchor=W)
    
    Remainder = TreeHigh % 20
    TreeviewPst = (TreeHigh-27.0) / (TreeLineNum * 20.0 + Remainder)
    BarStart = bar.get()[0]
    bar.set(BarStart,str(BarStart + TreeviewPst))    

# Treeview使用鼠标滚轮滚动后，自动调整另外两个Treeview的位置，并同步修改滚动条的位置
def TreeviewScroll(*Date):
    global TreeviewPst
    global TreeLineNum
    if(TreeLineNum == 666):
    	return
    
    if DegComBox:
        DegComBox.destroy()    
    if OpComBox:
        OpComBox.destroy()

    ParTreeview.yview('moveto',float(Date[0]))
    DegTreeview.yview('moveto',float(Date[0]))
    OpTreeview.yview('moveto',float(Date[0]))
    bar.set(Date[0],str(float(Date[0]) + TreeviewPst))    


#建立窗口
win = Tk()
win.title('Flying Driver')
win.geometry('450x550')
#win.iconbitmap('bitbug_favicon.ico')
#win.resizable(0,0) #阻止Python GUI的大小调擿

TopFrame = ttk.Frame(win)
TopFrame.pack(fill=X,padx=5,pady=5,expand=FALSE,side=TOP)

#创建单行文本框，输入地址使用
dir = StringVar()
dirEntry = ttk.Entry(TopFrame, textvariable=dir, width=20)
dirEntry.pack(fill=X,padx=0,pady=0,expand=TRUE,side=LEFT)
#dirEntered.insert(INSERT,"输入路径...")

# 创建按钮，用于输入地址使用
ViewButton = ttk.Button(TopFrame)
ViewButton.config(text='View',command=SelectFile,width =4)
ViewButton.pack(expand=FALSE,side=LEFT,padx=0,pady=0)

# 空白标签，占位分开view和echange按钮
SpaceLabel = ttk.Label(TopFrame)
SpaceLabel.config(width = 0)
SpaceLabel.pack(expand=FALSE,padx=5,pady=0,side=LEFT)

# 创建按钮，用于进行转换操作
ChgButton = ttk.Button(TopFrame)
ChgButton.config(text='Exchange',command=ChangeFile,width=8)
ChgButton.pack(expand=FALSE,side=RIGHT,padx=0,pady=0)

# 创建框架，用于摆放三个Treeview控件
BotFrame = ttk.Frame(win)
BotFrame.pack(fill=BOTH,padx=5,pady=5,expand=TRUE,side=TOP)

ParTreeview = ttk.Treeview(BotFrame)
ParTreeview.config(columns=('Parameter'),show='headings',yscrollcommand=TreeviewScroll)
ParTreeview.column('Parameter', width=150, anchor='w')
ParTreeview.heading('Parameter', text='Parameter')
ParTreeview.pack(expand=TRUE,fill=BOTH,padx=0,pady=0,side=LEFT)

DegTreeview = ttk.Treeview(BotFrame)
DegTreeview.config(columns=('Degree'),show='headings',yscrollcommand=TreeviewScroll)
DegTreeview.column('Degree', width=5, anchor='w')
DegTreeview.heading('Degree', text='Precision')
DegTreeview.pack(expand=TRUE,fill=BOTH,padx=0,pady=0,side=LEFT)

OpTreeview = ttk.Treeview(BotFrame)
OpTreeview.config(columns=('Operation'),show='headings',yscrollcommand=TreeviewScroll)
OpTreeview.column('Operation', width=5, anchor='w')
OpTreeview.heading('Operation', text='Operation')
OpTreeview.pack(expand=TRUE,fill=BOTH,padx=0,pady=0,side=LEFT)

# 创建滑块，用于控制三个Treeview的滚动
bar=ttk.Scrollbar(BotFrame)
bar.config(command=BarMove)#ParTreeview.yview)
bar.pack(fill=Y,side=RIGHT,expand=FALSE,padx=0,pady=0)

# 底部标签，显示当前的操作状态
InfoLabel = ttk.Label(win)
InfoLabel.config(text=('Drivering...'))
InfoLabel.pack(fill=X,expand=FALSE,padx=5,pady=0,side=BOTTOM)

# 初始化Treeview对应的三个List的值
for i in range(100):
    ParList.append('Par')
    DegList.append('保持')
    OpList.append('无操作')

# 窗口大小改变，需要改变滑块的大小
BotFrame.bind("<Configure>",BarSizeAutoSet)
#DegTreeview.bind("<Double-1>", DegDBClick)
#OpTreeview.bind("<Double-1>", OpDBClick)

# 绑定三个Treeview的点击操作，包括下拉框选择和当前选中条目的设置
ParTreeview.bind("<Button-1>",ParClick )
DegTreeview.bind("<Button-1>", DegClick)
DegTreeview.bind("<Double-1>", DegDbClear)
DegTreeview.bind("<ButtonRelease-1>", TreeButtonRelease)
OpTreeview.bind("<Button-1>",OpClick )
OpTreeview.bind("<Double-1>", OpDbClear)
OpTreeview.bind("<ButtonRelease-1>",TreeButtonRelease )

win.mainloop()

