## pyuic5 -o C:\Users\zhwsd\Desktop\py\ui_main.py C:\Users\zhwsd\Desktop\py\ui_main.ui 
##

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from ui_main import Ui_MainWindow
import copy

class Ui_ALL(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_ALL, self).__init__(parent=parent)
        self.uimain = Ui_MainWindow()
        self.uimain.setupUi(self)   # setupUi in ui_main.py

        self.uimain.pb_test.clicked.connect(self.submit)
        self.uimain.pb_LoadXls.clicked.connect(self.loadXls)
        self.uimain.pb_Exchange.clicked.connect(self.ChangeFile)

    def submit(self):
        self.uimain.textEdit.append('PushButton Pushed')
        self.uimain.textEdit.moveCursor(QtGui.QTextCursor.End)

    def loadXls(self):
        self.uimain.textEdit.append('loadXls Pushed')
        self.uimain.textEdit.moveCursor(QtGui.QTextCursor.End)

        filenametuple = QtWidgets.QFileDialog.getOpenFileName(self, 'open file')
        self.uimain.filename = filenametuple[0]      # tuple to string
        if self.uimain.filename == '':
            self.uimain.textEdit.append('No file select')
            self.uimain.textEdit.moveCursor(QtGui.QTextCursor.End) 
            return
        self.uimain.textEdit.append('SelectFile')
        self.uimain.textEdit.append(self.uimain.filename)
        self.uimain.textEdit.moveCursor(QtGui.QTextCursor.End) 
        # open the csv file
        with open(self.uimain.filename) as f_in:
            # lookup the line index of 时间
            self.uimain.read_raw = f_in.readlines()

            # find the "时间" row
            k = 0
            for line in self.uimain.read_raw:
                linelist = line.split(",")
                if linelist[0] == "时间":
                    self.uimain.timerowindex = k      # the line number of the varname 时间/ U2-00/...
                    self.uimain.varnum = len(linelist)
                    # print(linelist)
                    break                   # break when linelist is the varname 时间/ U2-00/...
                k = k + 1

            self.uimain.tableWidget.setRowCount(self.uimain.varnum)
            # self.uimain.tableWidget.setColumnCount(3)
            self.uimain.tableWidget.setVerticalHeaderLabels(linelist)

    def ChangeFile(self):
        self.uimain.textEdit.append('ChangeFile')
        self.uimain.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.uimain.read_ripe = copy.copy(self.uimain.read_raw)
        for i_line in range(self.uimain.varnum - 1):
            # modify the data
            # ifneedchange:
            # waiting: 下面这句还存在问题,不知道为什么无法取出这个格子的数据
            strselect = self.uimain.tableWidget.item(i_line, 1).text() 
            if strselect == '1' :
                prsition = 1    # Precision[temp]
                for i_row in range(self.uimain.timerowindex + 1, len(self.uimain.read_ripe)):  #read_raw[( + 1):]:
                    rowlist = self.uimain.read_ripe[i_row].split(",")
                    value = float(rowlist[i_line])
                    if value < 0:
                        value = value + 65536 * prsition
                        value = round(value, 3)
                    elif value > 32767 * prsition:
                        value = value - 65536 * prsition
                        value = round(value, 3)
                    rowlist[i_line] = str(value)
                    self.uimain.read_ripe[i_row] = ','.join(rowlist)
                
                self.uimain.textEdit.append('Dealing' + str(i_line))
                self.uimain.textEdit.moveCursor(QtGui.QTextCursor.End)

        with open(self.uimain.filename + 'change.csv', 'w') as f_out:
            f_out.writelines(self.uimain.read_ripe)
 


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    uiall = Ui_ALL()
    uiall.show()
    sys.exit(app.exec_())
