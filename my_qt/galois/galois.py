from PyQt5 import QtCore, QtGui, QtWidgets
from galois_view import Ui_MainWindow
import pyqtgraph as pg
import numpy as np
import sys
import GA
import pdb


def run():
    global application
    timer = pg.QtCore.QTimer(application)
    timer.timeout.connect(application.updateCurveData)
    timer.start(500)



class GeneticAlgoithm:
    def __init__(self):
        self.pop_size  = (20,2)
        self.parent_population = np.random.normal(-2.0,0.1,self.pop_size)
        self.ELITIST_PERCENT = 0.1
        self.POPULATION = 20
        self.CHROME_LENGTH = 2

    def getGeneticAlgorithmData(self):

            fitness = GA.get_population_fitness(self.parent_population)
            result = np.where(fitness==max(fitness))
            temp_point = self.parent_population[result[0][0]]
            parents = GA.select_mating_pool(self.parent_population, fitness,
                                            int(self.ELITIST_PERCENT*self.POPULATION))
            offspring_crossover = GA.crossover(parents,
                                            offspring_size=(self.pop_size[0]-parents.shape[0], self.CHROME_LENGTH))
            offspring_mutation = GA.mutation(offspring_crossover)
            self.parent_population[0:parents.shape[0], :] = parents
            self.parent_population[parents.shape[0]:, :] = offspring_mutation
            return temp_point


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.graphicsView.setLabel('left', 'Value', units='1')
        self.ui.graphicsView.setLabel('bottom', 'Value', units='1')
        self.ui.graphicsView.setXRange(-2, 2)
        self.ui.graphicsView.setYRange(-2, 2)
        self.ui.graphicsView.setTitle("Search Position")
        self.ui.actionGenetic_Algorithm.triggered.connect(run)


    def my_scatter_plot(self):
        self.dataX = []
        self.dataY = []
        self.idx = 0
        self.N = 10

        self.scatter =  pg.ScatterPlotItem()
        self.ui.graphicsView.addItem(self.scatter,title="GA")


    def updateCurveData(self):

        global ga
        temp_point = ga.getGeneticAlgorithmData()
        print(len(self.dataX))
        if(len(self.dataX)<self.N):
            self.dataX.append(temp_point[0])
            self.dataY.append(temp_point[1])
        else:
            self.dataX[:-1] = self.dataX[1:]
            self.dataX[-1] = temp_point[0]
            self.dataY[:-1] = self.dataY[1:]
            self.dataY[-1] = temp_point[1]

        self.scatter.setData(self.dataX,self.dataY)

        self.idx+=1
        print(self.dataY)
        print(self.idx)


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
ga = GeneticAlgoithm()

application.my_scatter_plot()
sys.exit(app.exec())





