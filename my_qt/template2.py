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
from view2 import Ui_MainWindow



class Control_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Control_MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        pw = pg.PlotWidget(name="plot1")
        #self.ui.verticalLayout.addWidget(pw)
        pw.setLabel('left', 'Value', units='V')
        pw.setLabel('bottom', 'Time', units='s')
        pw.setXRange(0, 10)
        pw.setYRange(0, 10)

        pw2 = pg.PlotWidget(name="plot2")
        #self.ui.verticalLayout.addWidget(pw2)
        pw.setLabel('left', 'Value', units='T')
        pw.setLabel('bottom', 'Time', units='W')
        pw.setXRange(2, 4)
        pw.setYRange(2, 4)

       vals = np.random.normal(loc=4,size=400)
       y = pg.pseudoScatter(vals)










if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = Control_MainWindow()
    application.show()
    sys.exit(app.exec_())
    pass

