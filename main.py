import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from ui_main import Ui_MainWindow
    
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

        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'open file')
        filename = filename[0]      # tuple to string
        if filename == '':
            self.uimain.textEdit.append('No file select')
            self.uimain.textEdit.moveCursor(QtGui.QTextCursor.End) 
            return
        self.uimain.textEdit.append('SelectFile')
        self.uimain.textEdit.append(filename)
        self.uimain.textEdit.moveCursor(QtGui.QTextCursor.End) 
        # open the csv file
        with open(filename) as f_in:
            # lookup the line index of 时间
            read_raw = f_in.readlines()
            read_ripe = read_raw

            # find the "时间" row
            k = 0
            for line in read_raw:
                linelist = line.split(",")
                if linelist[0] == "时间":
                    lineindex_time = k      # the line number of the varname 时间/ U2-00/...
                    varnum = len(linelist)
                    # print(linelist)
                    break                   # break when linelist is the varname 时间/ U2-00/...
                k = k + 1

            # self.uimain.tableWidget.setRowCount = varnum
            self.uimain.tableWidget.setVerticalHeaderLabels(linelist)


    def ChangeFile(self):
        self.uimain.textEdit.append('ChangeFile')
        self.uimain.textEdit.moveCursor(QtGui.QTextCursor.End)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    uiall = Ui_ALL()
    uiall.show()
    sys.exit(app.exec_())
