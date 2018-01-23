from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg, uic
import numpy
import time
import os.path
from wator import WaTor
from .gridwidgetclass import GridWidget

CELL_SIZE = 32


def pixel_to_logical(x, y):
    """
    Convert pixels from grid to logical rows and columns to numpy
    
    :param: ``x`` Number of pixels in x axis.
    :param: ``y`` Number of pixels in y axis.
    :return: ``x, y`` Logical rows and columns.
    """
    return y // CELL_SIZE, x // CELL_SIZE


def logical_to_pixel(row, column):
    """
    Convert logical rows and columns from numpy to pixels to display
    
    :param: ``row`` Number of rows.
    :param: ``cols`` Number of columns.
    :return: ``cols, rows`` Pixels to display.
    """
    return column * CELL_SIZE, row * CELL_SIZE


def start_dialog(window, grid):
    """
    Open dialog at start of program.
    
    :param: ``window`` Main window of application.
    :param: ``grid`` Layout of window.
    :return: ``None`` 
    """
    dialog = QtWidgets.QDialog(window)

    with open('wator/gui/start.ui') as f:
        uic.loadUi(f, dialog)

    action1 = dialog.findChild(QtWidgets.QPushButton, 'newButton')
    action1.clicked.connect(lambda: new_dialog(window, grid))

    action2 = dialog.findChild(QtWidgets.QPushButton, 'openButton')
    action2.clicked.connect(lambda: open_dialog(window, grid))

    result = dialog.exec()

    if result == QtWidgets.QDialog.Rejected:
        return
    if result == QtWidgets.QDialog.Accepted:
        return




def new_dialog(window, grid):
    """
    Open dialog for creating new simulation array.
    
    User can enter number of cols and rows, number of fish and number of sharks. Function create arrays (creatures and energies) and update a grid.
    
    :param: ``window`` Main window of application.
    :param: ``grid`` Layout of window.
    :return: ``None`` 
    """
    # Create new dialog over main window
    dialog = QtWidgets.QDialog(window)

    # Load layout from Qt Designer.
    with open('wator/gui/newsimulation.ui') as f:
        uic.loadUi(f, dialog)

    # Display dialog.
    # Function exec - what it do?: user can't use rest of application till dialog is open
    result = dialog.exec()

    # Result - if user reject a dialog or not
    if result == QtWidgets.QDialog.Rejected:
        return

    # Load values from SpinBoxs
    cols = dialog.findChild(QtWidgets.QSpinBox, 'colsBox').value()
    rows = dialog.findChild(QtWidgets.QSpinBox, 'rowsBox').value()
    nfish = dialog.findChild(QtWidgets.QSpinBox, 'nfishBox').value()
    nsharks = dialog.findChild(QtWidgets.QSpinBox, 'nsharksBox').value()

    if cols == 0 or rows == 0:
       error = QtWidgets.QErrorMessage()
       error.showMessage('Number of columns or rows can\'t be 0!')
       error.exec()
       return

    wator = WaTor(shape=(rows, cols), nfish=nfish, nsharks=nsharks)
    # Create new map
    grid.array = wator.creatures
    grid.energy = wator.energies

    # Change size of array
    size = logical_to_pixel(rows, cols)
    grid.setMinimumSize(*size)
    grid.setMaximumSize(*size)
    grid.resize(*size)

    # Rewrite of grid
    grid.update()


def save_dialog(window, grid):    
    """
    Open dialog for saving simulation array.
    
    User can enter a path to folder where to save a file with simulation. 
    
    :param: ``window`` Main window of application.
    :param: ``grid`` Layout of window.
    :return: ``None`` 
    """
    dialog = QtWidgets.QDialog(window)

    #with open('wator/gui/savesimulation.ui') as f:
    #    uic.loadUi(f, dialog)

    #result = dialog.exec()

    #if result == QtWidgets.QDialog.Rejected:
    #    return

    filename, _filter = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", grid.filepath, "(*)")
    #filename = dialog.findChild(QtWidgets.QLineEdit, 'filenameLine').text()

    if filename == "":
       return

    #if os.path.isfile(filename):
    #   error = QtWidgets.QMessageBox.critical(None, "Error", "File already exist!")
    #   error.exec()
    #   return

    count = len(filename.split('/')[-1])
    grid.filepath = filename[:-count] 

    numpy.savetxt(filename, grid.array)



def open_dialog(window, grid):
    """
    Open dialog for opening simulation array.
    
    User can enter a path to filder where simulation is saved and select file to open. Function read file, create arrays (creatures and energies) and update a grid.
    
    :param: ``window`` Main window of application.
    :param: ``grid`` Layout of window.
    :return: ``None`` 
    """
    dialog = QtWidgets.QDialog(window)

    #with open('wator/gui/opensimulation.ui') as f:
    #    uic.loadUi(f, dialog)

    #result = dialog.exec()

    #if result == QtWidgets.QDialog.Rejected:
    #    return

    filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open file", grid.filepath, "(*)")
    #filename = dialog.findChild(QtWidgets.QLineEdit, 'filenameLine').text()

    if filename == "":
       return

    #if not os.path.isfile(filename):
       #error = QtWidgets.QErrorMessage()
       #error.showMessage('File does not exist!')
     #  error = QtWidgets.QMessageBox.critical(None, "Error", "File does not exist!", QtWidgets.QMessageBox.Ok)
      # error.exec()
       #return

    if os.path.getsize(filename) == 0:
       error = QtWidgets.QMessageBox.critical(None, "Error", "File is empty!", QtWidgets.QMessageBox.Ok)
     #  error = QtWidgets.QErrorMessage()
     #  error.showMessage('File is empty!')
     #  error.exec()
       return

    try:
       array = numpy.loadtxt(filename, dtype=numpy.int8)
    except ValueError:
       #error = QtWidgets.QErrorMessage()
       #error.showMessage('File does not contains data for simulation!')
       #error.exec()
       error = QtWidgets.QMessageBox.critical(None, "Error", "File does not contains data for simulation!", QtWidgets.QMessageBox.Ok)
       return


    wator = WaTor(creatures=array)
    grid.array = wator.creatures
    grid.energy = wator.energies

    size = logical_to_pixel(grid.array.shape[0], grid.array.shape[1])
    grid.setMinimumSize(*size)
    grid.setMaximumSize(*size)
    grid.resize(*size)

    count = len(filename.split('/')[-1])
    grid.filepath = filename[:-count]

    grid.update()


def print_about(window, grid):
    """
    Open window with information about application.
    
    :param: ``window`` Main window of application.
    :param: ``grid`` Layout of window.
    :return: ``None`` 
    """
    about = QtWidgets.QMessageBox.about(None, "About WaTor", "<b>WaTor Simulations</b><br>Python module with GUI simulating WaTor sea world<br><br>2017<br>Author: Lenka Stejskalova<br><a href=\"https://github.com/stejsle1/wator\">GitHub stejsle1/wator</a><br>Contains <a href=\"https://pypi.python.org/pypi/PyQt5/5.9.1\">PyQt5</a> and graphics from <a href=\"opengameart.org\">OpenGameArt.org</a>")
    return

