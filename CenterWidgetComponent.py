#!/usr/bin/Python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication,QPushButton, QWidget, QGridLayout, QInputDialog,QTextBrowser, QLabel, QLineEdit, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import GetStockData as gd
import SA_AnasyisMethod as SA

class DataManagement(QWidget):
    def __init__(self, parent = None):
        super(DataManagement, self).__init__(parent)
        self.initUI()
        self.show()
    def initUI(self):
        self.setWindowIcon(QIcon('DBM.jpg'))
        self.resize(300,200)
        updateButton = QPushButton('Update Data', self)
        creatButton = QPushButton('Creat Table',self)
        updateAllButton = QPushButton('Update all',self)
        updateButton.clicked.connect(self.UpateTableInDB)
        creatButton.clicked.connect(self.CreatTableInDB)
        updateAllButton.clicked.connect(self.UpdateAll)
        messagelabe = QLabel('message')
        self.messageView = QTextBrowser()
        tableLabel = QLabel('tables')
        self.tableView = QTextBrowser()
        self.AppendTableNames(self.tableView)
        mainLayout = QGridLayout()
        mainLayout.setSpacing(1)
        mainLayout.addWidget(updateButton,1,0)
        mainLayout.addWidget(creatButton,1,1)
        mainLayout.addWidget(updateAllButton,1,2)
        mainLayout.addWidget(messagelabe,2,0)
        mainLayout.addWidget(tableLabel,2,1)
        mainLayout.addWidget(self.messageView,3,0,5,1)
        mainLayout.addWidget(self.tableView,3,1,5,1)
        self.setLayout(mainLayout)

    def CreatTableInDB(self):
        self.askStockcode = QInputDialog()
        text, ok = self.askStockcode.getText(self, 'Input Stock Code', 'Enter Stock Code:')
        if ok:
            stockCode = str(text)
            message = 'loading:' + stockCode
            self.messageView.append(message)
            gd.CreatTableInDB(stockCode)
            self.messageView.append("Done")
            self.tableView.append(stockCode)
        return
    def UpateTableInDB(self):
        self.askStockcode = QInputDialog()
        text, ok = self.askStockcode.getText(self, 'Input Stock Code', 'Enter Stock Code:')
        if ok:
            stockCode = str(text)
            message = 'updateing:' + stockCode
            self.messageView.append(message)
            gd.UpdateTableInDB(stockCode)
            self.messageView.append("Done")
        return
    def UpdateAll(self):
        stocks = gd.GetAllTableNameInDB()
        for code in stocks:
            message = 'loading:' + code
            self.messageView.append(message)
            gd.UpdateTableInDB(code)
            self.messageView.append("Done")
    def AppendTableNames(self,tableView):
        stocks = gd.GetAllTableNameInDB()
        for code in stocks:
            tableView.append(code)
        return

class Nearest_anasys(QWidget):
    def __init__(self, parent = None):
        super(Nearest_anasys, self).__init__(parent)
        self.initUI()
        self.show()
        return
    def initUI(self):
        self.setWindowIcon(QIcon('DBM.jpg'))
        self.resize(300, 200)
        codeLabel = QLabel("Stock Code:")
        n_neigboursLabel = QLabel("Neibours Count:")
        self.codeLine = QLineEdit()
        self.countLine = QLineEdit()
        runButton = QPushButton("Run")
        runButton.clicked.connect(self.on_run)
        mainLayout = QGridLayout()
        mainLayout.setSpacing(1)
        mainLayout.addWidget(codeLabel, 1, 0)
        mainLayout.addWidget(self.codeLine, 1, 1)
        mainLayout.addWidget(n_neigboursLabel,2, 0)
        mainLayout.addWidget(self.countLine,2, 1)
        mainLayout.addWidget(runButton,3,1)
        self.setLayout(mainLayout)
        return

    def on_run(self):
        stockCode = str(self.codeLine.text())
        kNeighbors = int(self.countLine.text())
        anasyisor = SA.AnalysisDirector()
        method = SA.Nearest_Neighbors_MethodBuilder(code = stockCode, kNeighbors= kNeighbors)
        anasyisor.methodBuilder = method
        anasyisor.Analysis()
        return

class Wavelets_anasys(QWidget):
    def __init__(self, parent = None):
        super(Wavelets_anasys, self).__init__(parent)
        self.initUI()
        self.show()
        return

    def initUI(self):
        self.setWindowIcon(QIcon('DBM.jpg'))
        self.resize(300, 200)
        codeLabel = QLabel("Stock Code:")
        level = QLabel("Level:")
        days = QLabel("Data Count:")
        self.codeLine = QLineEdit()
        self.levelLine = QLineEdit()
        self.daysLine = QLineEdit()
        self.db1Option = QRadioButton('db1')
        self.db2Option = QRadioButton('db2')
        self.haarOption = QRadioButton('haar')
        runButton = QPushButton('Run')
        runButton.clicked.connect(self.on_run)
        mainLayout = QGridLayout()
        mainLayout.addWidget(codeLabel,0,1)
        mainLayout.addWidget(self.codeLine,0,2)
        mainLayout.addWidget(level, 1, 1)
        mainLayout.addWidget(days, 2, 1)
        mainLayout.addWidget(self.daysLine,2,2)
        mainLayout.addWidget(self.levelLine,1,2)
        mainLayout.addWidget(self.db1Option, 0,0)
        mainLayout.addWidget(self.db2Option,1,0)
        mainLayout.addWidget(self.haarOption,2,0)
        mainLayout.addWidget(runButton, 3, 2)
        mainLayout.setSpacing(30)
        self.setLayout(mainLayout)
    def on_run(self):
        stockCode = str(self.codeLine.text())
        level = int(self.levelLine.text())
        days = int(self.daysLine.text())
        waveletsType = self.CheckType()
        if level > 7 or waveletsType == None:
            return
        anasyisor = SA.AnalysisDirector()
        method = SA.Wavelets_MethodBuilder(code = stockCode, days = days, type=waveletsType,level = level)
        anasyisor.methodBuilder = method
        anasyisor.Analysis()
        return
    def CheckType(self):
        if self.db1Option.isChecked():
            return 'db1'
        elif self.db2Option.isChecked():
            return 'db2'
        elif self.haarOption.isChecked():
            return 'haar'
        else:
            return None

class Correlation_anasys(QWidget):
    def __init__(self, parent = None):
        super(Correlation_anasys, self).__init__(parent)
        self.initUI()
        self.show()
        return

    def initUI(self):
        self.setWindowIcon(QIcon('DBM.jpg'))
        self.resize(300, 200)
        code1Label = QLabel("First Stock Code:")
        code2Label = QLabel("Second Stock Code:")
        levelLabel = QLabel("confidence Level:")
        daysLabel = QLabel("Data Count:")
        displayCountLabel = QLabel("Display Price Count:")
        self.code1Line = QLineEdit()
        self.code2Line = QLineEdit()
        self.levelLine = QLineEdit()
        self.daysLine = QLineEdit()
        self.displayLine = QLineEdit()
        runButton = QPushButton('Run')
        runButton.clicked.connect(self.on_run)
        mainLayout = QGridLayout()
        mainLayout.addWidget(code1Label, 0, 0)
        mainLayout.addWidget(code2Label, 1, 0)
        mainLayout.addWidget(levelLabel, 2, 0)
        mainLayout.addWidget(daysLabel, 3, 0)
        mainLayout.addWidget(displayCountLabel, 4, 0)
        mainLayout.addWidget(self.code1Line, 0, 1)
        mainLayout.addWidget(self.code2Line, 1, 1)
        mainLayout.addWidget(self.levelLine, 2, 1)
        mainLayout.addWidget(self.daysLine, 3, 1)
        mainLayout.addWidget(self.displayLine, 4, 1)
        mainLayout.addWidget(runButton, 5, 1)
        mainLayout.setSpacing(1)
        self.setLayout(mainLayout)
        return
    def on_run(self):
        stockCode1 = str(self.code1Line.text())
        stockCode2 = str(self.code2Line.text())
        level = float(self.levelLine.text())
        days = int(self.daysLine.text())
        display = int(self.displayLine.text())
        if level > 1 or days == None:
            return
        if display < 0:
            display = 0
        anasyisor = SA.AnalysisDirector()
        method = SA.Correlation_MethodBuilder(code1 = stockCode1, code2 = stockCode2,days=days,display=display, confidenceLevel = level)
        anasyisor.methodBuilder = method
        anasyisor.Analysis()
        return





if __name__ == '__main__':
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        test = Correlation_anasys()
        #test = AskStockCodeDialog()
        sys.exit(app.exec_())


