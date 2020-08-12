# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
import sys
import pyqtgraph as pg
import numpy as np
from view import Ui_MainWindow


def run():
    global application
    timer = pg.QtCore.QTimer(application)
    timer.timeout.connect(application.updateCurveData)
    timer.start(50)

class Control_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Control_MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(run)


    def my_scatter_plot(self):
        self.dataX = []
        self.dataY = []
        self.idx = 0
        self.N = 200

        # setting the graph
        self.ui.graphicsView.setXRange(0,10)
        self.ui.graphicsView.setYRange(0,10)


        self.scatter =  pg.ScatterPlotItem()
        self.ui.graphicsView.addItem(self.scatter,title="GA")

    def updateCurveData(self):
        tmpX = np.random.randint(1,10,1)[0]
        tmpY = np.random.randint(1,10,1)[0]
        if(len(self.dataX)<self.N):
            self.dataX.append(tmpX)
            self.dataY.append(tmpY)
        else:
            self.dataX[:-1] = self.dataX[1:]
            self.dataX[-1] = tmpX
            self.dataY[:-1] = self.dataY[1:]
            self.dataY[-1] = tmpY

        self.idx+=1
        self.scatter.setData(self.dataX,self.dataY)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = Control_MainWindow()
    application.show()
    application.my_scatter_plot()
    sys.exit(app.exec_())
    pass

