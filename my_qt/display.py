# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'display.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import pyqtgraph as pg
import numpy as np

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(240, 180, 291, 211))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # my define
#        self.graphics_layout = self.graphicsView.layout()
        self.plot_plt = pg.PlotWidget()
        self.graphicsView.setViewport(self.plot_plt)

        # plot the graph
        self.dataX = []
        self.dataY = []
        self.idx = 0
        self.N = 200
        #self.plot_plt.plot([2,3,4],[3,4,1])



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def updatecurvedata(self):
        tmpX = np.random.randint(0,10,1)[0]
        tmpY = np.random.randint(0,10,1)[0]
        if(len(self.dataX)<self.N):
            self.dataX.append(tmpX)
            self.dataY.append(tmpY)
        else:
            self.dataX[:-1] = self.dataX[1:]
            self.dataX[-1] = tmpX
            self.dataY[:-1] = self.dataY[1:]
            self.dataY[-1] = tmpY

        self.plot_plt.plot().setData(self.dataX,self.dataY)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(ui.updatecurvedata)
    timer.start(50)

    sys.exit(app.exec_())
    pass
