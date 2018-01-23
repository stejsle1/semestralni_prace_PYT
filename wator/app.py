from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg, uic
import numpy
import time
import os.path
from wator import WaTor
from .windows import start_dialog, new_dialog, save_dialog, open_dialog, print_about
from .simulations import next_chronon, simulation_loop, simulation_opti
from .gridwidgetclass import GridWidget
from .matplot import MyMplCanvas


CELL_SIZE = 32

SVG_WATER = QtSvg.QSvgRenderer('wator/gui/water.svg')
SVG_FISH = QtSvg.QSvgRenderer('wator/gui/fish.svg')
SVG_SHARK = QtSvg.QSvgRenderer('wator/gui/shark.svg')

VALUE_ROLE = QtCore.Qt.UserRole

def pixels_to_logical(x, y):
    """
    Convert pixels from grid to logical rows and columns to numpy.
    
    :param: ``x`` Number of pixels in x axis.
    :param: ``y`` Number of pixels in y axis.
    :return: ``x, y`` Logical rows and columns.
    """
    return y // CELL_SIZE, x // CELL_SIZE


def logical_to_pixels(row, column):
    """
    Convert logical rows and columns from numpy to pixels to display.
    
    :param: ``row`` Number of rows.
    :param: ``cols`` Number of columns.
    :return: ``cols, rows`` Pixels to display.
    """
    return column * CELL_SIZE, row * CELL_SIZE

def main():
    """Main function.

       Run GUI app.
    """
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()

    with open('wator/gui/mainwindow.ui') as f:
        uic.loadUi(f, window)

    # Wator instance = grid; - random creatures setting
    wator = WaTor(numpy.zeros((20, 20)), numpy.zeros((20, 20)))


    # Get scrollArea from Qt Designeru
    scroll_area = window.findChild(QtWidgets.QScrollArea, 'scrollArea')
    # Put grid in it
    grid = GridWidget(wator.creatures, wator.energies)
    scroll_area.setWidget(grid)
    
    
     # Get graph from Qt Designeru
    graph_area = window.findChild(QtWidgets.QHBoxLayout, 'plotLayout')
    # Put grid in it
    canvas = MyMplCanvas(window, width=5, height=1, dpi=75)
    graph_area.addWidget(canvas)

    
    # Get palette from Qt Designeru
    palette = window.findChild(QtWidgets.QListWidget, 'palette')

    for name, svg, num in ('Water', 'wator/gui/water.svg', 0),('Fish', 'wator/gui/fish.svg', 1),('Shark', 'wator/gui/shark.svg', -1):
       item = QtWidgets.QListWidgetItem(name)  # make item
       icon = QtGui.QIcon(svg)  # icon
       item.setIcon(icon)  # put icon to item
       item.setData(VALUE_ROLE, num)
       palette.addItem(item)  # put item to palette


    def item_activated():
        """
        This function is called when user pick an item
        
        :return: ``None``
        """

        for item in palette.selectedItems():
            grid.selected = item.data(VALUE_ROLE)

    palette.itemSelectionChanged.connect(item_activated)
    palette.setCurrentRow(0)


    # Connect signal actionNew.triggered
    action1 = window.findChild(QtWidgets.QAction, 'actionNew')
    action1.triggered.connect(lambda: new_dialog(window, grid))

    action2 = window.findChild(QtWidgets.QAction, 'actionNext_chronon')
    action2.triggered.connect(lambda: next_chronon(window, grid))

    action3 = window.findChild(QtWidgets.QAction, 'actionSave')
    action3.triggered.connect(lambda: save_dialog(window, grid))

    action4 = window.findChild(QtWidgets.QAction, 'actionOpen')
    action4.triggered.connect(lambda: open_dialog(window, grid))

    action5 = window.findChild(QtWidgets.QAction, 'actionSim')
    action5.triggered.connect(lambda: simulation_loop(window, grid, app))

    action6 = window.findChild(QtWidgets.QAction, 'actionOpti_sim')
    action6.triggered.connect(lambda: simulation_opti(window, grid, app, canvas))

    action7 = window.findChild(QtWidgets.QAction, 'actionAbout')
    action7.triggered.connect(lambda: print_about(window, grid))

    init = window.findChild(QtWidgets.QSpinBox, 'energy_initialBox').value()
    grid.initEnergy = init
    
    window.show()

    # Open start dialog - "the crossroads"
    start_dialog(window, grid)


    return app.exec()

if __name__ == "__main__":
    main()
