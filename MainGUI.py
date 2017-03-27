#!/usr/bin/Python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QGridLayout, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QRect
from CenterWidgetComponent import DataManagement, Nearest_anasys, Wavelets_anasys, Correlation_anasys

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.initUI()
        return

    def initUI(self):
        self.setWindowTitle('SA')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.resize(400,300)
        self.setCentralWidget(self.centerWidget())
        #self.statusBar().showMessage('testing')
        self.show()
        return

    def centerWidget(self):
        tabWidget = QTabWidget()
        dataWidget = DataManagement()
        nearest_anasysWidget = Nearest_anasys()
        WaveletWidget = Wavelets_anasys()
        tabWidget.addTab(dataWidget,"DataMangement")
        tabWidget.addTab(nearest_anasysWidget,"Nearest_Anasys")
        tabWidget.addTab(WaveletWidget, "Wavelets_Anasys")
        return tabWidget

class MainWindowTest(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.initUI()
        return

    def initUI(self):
        self.setWindowTitle('SA')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.resize(620,620)
        self.setCentralWidget(self.centerWidget())
        #self.statusBar().showMessage('testing')
        self.show()
        return

    def centerWidget(self):
        centerWidget = QWidget()
        dataIcon = QIcon('data.jpg')
        knnIcon = QIcon('knn.jpg')
        waveletsIcon = QIcon('wavelets.png')
        linerIcon = QIcon('liner.jpg')
        centerWidget.resize(600,600)
        button1 = QPushButton()
        button2 = QPushButton()
        button3 = QPushButton()
        button4 = QPushButton()
        button1.setStyleSheet('''background-image:url(green.jpg)''')
        button2.setStyleSheet('''background-image:url(green.jpg)''')
        button3.setStyleSheet('''background-image:url(green.jpg)''')
        button4.setStyleSheet('''background-image:url(green.jpg)''')
        button1.setIcon(dataIcon)
        button1.setIconSize(QSize(300,300))
        button1.clicked.connect(self.button1)
        button2.clicked.connect(self.button2)
        button3.clicked.connect(self.button3)
        button4.clicked.connect(self.button4)
        button2.setIcon(knnIcon)
        button2.setIconSize(QSize(300, 300))
        button3.setIcon(waveletsIcon)
        button3.setIconSize(QSize(300, 300))
        button4.setIcon(linerIcon)
        button4.setIconSize(QSize(300, 300))
        mainLayout = QGridLayout()
        mainLayout.addWidget(button1, 0, 0)
        mainLayout.addWidget(button2, 0, 1)
        mainLayout.addWidget(button3, 1, 0)
        mainLayout.addWidget(button4, 1, 1)
        centerWidget.setLayout(mainLayout)
        return centerWidget
    def button1(self):
        self.dataWidget = DataManagement()
        self.dataWidget.setWindowTitle('DataManagement')
        return
    def button2(self):
        self.nearestWidget = Nearest_anasys()
        self.nearestWidget.setWindowTitle('Nearest_anasys')
        return
    def button3(self):
        self.waveletsWidget = Wavelets_anasys()
        self.waveletsWidget.setWindowTitle('Wavelets_anasys')
        return
    def button4(self):
        self.correlationWidget = Correlation_anasys()
        self.correlationWidget.setWindowTitle('Correlation_anasys')
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindowTest()
    sys.exit(app.exec_())
