from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from wator import WaTor
import random
import matplotlib
from numpy import arange, sin, pi
from PyQt5 import QtCore, QtWidgets


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        self.axes.set_xticks([])
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['bottom'].set_visible(False)
        self.axes.spines['left'].set_visible(False)

        self.counter = 0
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Count')

    def update_figure(self):
        with open('wator/gui/simulations/logmatplot.txt', 'r+') as f:
            lines = f.readlines()
        x = [line.split()[0] for line in lines]
        y = [line.split()[1] for line in lines]
        a = [line.split()[2] for line in lines]
        b = [line.split()[3] for line in lines]

        if self.counter < 30: 
            self.counter += 1
        self.axes.plot(range(0, self.counter), x, 'r--')
        self.axes.plot(range(0, self.counter), y, 'b--')
        self.axes.plot(a, 'ro')
        self.axes.plot(b, 'bo')

        self.axes.set_xticks([])
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['bottom'].set_visible(False)
        self.axes.spines['left'].set_visible(False)

        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Count')
        self.draw()
