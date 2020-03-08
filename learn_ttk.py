import tkinter as tk
from tkinter import ttk  # �����ڲ���
import copy


li = ['王记','12','男']


win = tk.Tk()

tree = ttk.Treeview(win,columns=['1','2','3'],show='headings')
tree.column('1',width=100,anchor='center')
tree.column('2',width=100,anchor='center')
tree.column('3',width=100,anchor='center')
tree.heading('1',text='name')
tree.heading('2',text='学号')
tree.heading('3',text='其他')
tree.insert('','end',values=li)
tree.insert('','end',values=li)
tree.grid()


win.mainloop()