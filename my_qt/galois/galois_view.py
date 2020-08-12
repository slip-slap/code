# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galois.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(170, 80, 451, 371))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionGenetic_Algorithm = QtWidgets.QAction(MainWindow)
        self.actionGenetic_Algorithm.setObjectName("actionGenetic_Algorithm")
        self.actionRandom_Walk = QtWidgets.QAction(MainWindow)
        self.actionRandom_Walk.setObjectName("actionRandom_Walk")
        self.actionSimmulated_Annealing = QtWidgets.QAction(MainWindow)
        self.actionSimmulated_Annealing.setObjectName("actionSimmulated_Annealing")
        self.menuFile.addAction(self.actionOpen)
        self.menuRun.addAction(self.actionGenetic_Algorithm)
        self.menuRun.addAction(self.actionRandom_Walk)
        self.menuRun.addAction(self.actionSimmulated_Annealing)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuRun.setTitle(_translate("MainWindow", "Run"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionGenetic_Algorithm.setText(_translate("MainWindow", "Genetic Algorithm"))
        self.actionRandom_Walk.setText(_translate("MainWindow", "Random Walk"))
        self.actionSimmulated_Annealing.setText(_translate("MainWindow", "Simmulated Annealing"))

from pyqtgraph import PlotWidget
