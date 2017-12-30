from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg, uic
import numpy
import time
import os.path
from wator import WaTor
from .gridwidgetclass import GridWidget

CELL_SIZE = 32


def pixel_to_logical(x, y):
    """Convert pixels from grid to logical rows and columns to numpy"""
    return y // CELL_SIZE, x // CELL_SIZE


def logical_to_pixel(row, column):
    """Convert logical rows and columns from numpy to pixels to display"""
    return column * CELL_SIZE, row * CELL_SIZE



def new_dialog(window, grid):
    # Vytvorime novy dialog.
    # V dokumentaci maji dialogy jako argument `this`;
    # jde o "nadrazene" okno.
    dialog = QtWidgets.QDialog(window)

    # Nacteme layout z Qt Designeru.
    with open('wator/gui/newsimulation.ui') as f:
        uic.loadUi(f, dialog)

    # Zobrazime dialog.
    # Funkce exec zajisti modalitu (tzn. nejde ovladat zbytek aplikace,
    # dokud je dialog zobrazen) a vrati se az potom, co uzivatel dialog zavre.
    result = dialog.exec()

    # Vysledna hodnota odpovida tlacitku/zpusobu, kterym uzivatel dialog zavrel.
    if result == QtWidgets.QDialog.Rejected:
        # Dialog uzivatel zavrel nebo klikl na Cancel.
        return

    # Nacteni hodnot ze SpinBoxu
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
    # Vytvoreni nove mapy
    grid.array = wator.creatures
    grid.energy = wator.energies

    # Mapa muze byt jinak velka, tak musime zmenit velikost Gridu;
    # (tento kod pouzivame i jinde, meli bychom si na to udelat funkci!)
    size = logical_to_pixel(rows, cols)
    grid.setMinimumSize(*size)
    grid.setMaximumSize(*size)
    grid.resize(*size)

    # Prekresleni celeho Gridu
    grid.update()


def save_dialog(window, grid):
    dialog = QtWidgets.QDialog(window)

    #with open('wator/gui/savesimulation.ui') as f:
    #    uic.loadUi(f, dialog)

    #result = dialog.exec()

    #if result == QtWidgets.QDialog.Rejected:
    #    return

    filename, _filter = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "wator/gui/simulations/", "(*)")
    #filename = dialog.findChild(QtWidgets.QLineEdit, 'filenameLine').text()

    if filename == "":
       return

    #if os.path.isfile(filename):
    #   error = QtWidgets.QMessageBox.critical(None, "Error", "File already exist!")
    #   error.exec()
    #   return

    numpy.savetxt(filename, grid.array)



def open_dialog(window, grid):
    dialog = QtWidgets.QDialog(window)

    #with open('wator/gui/opensimulation.ui') as f:
    #    uic.loadUi(f, dialog)

    #result = dialog.exec()

    #if result == QtWidgets.QDialog.Rejected:
    #    return

    filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open file", 'wator/gui/simulations/', "(*)")
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

    size = logical_to_pixels(grid.array.shape[0], grid.array.shape[1])
    grid.setMinimumSize(*size)
    grid.setMaximumSize(*size)
    grid.resize(*size)

    grid.update()


def print_about(window, grid):
    about = QtWidgets.QMessageBox.about(None, "About WaTor", "<b>WaTor simulation</b><br>Python module with GUI simulating WaTor sea world<br><br>2017<br>Author: Lenka Stejskalova<br><a href=\"https://github.com/stejsle1/wator\">GitHub stejsle1/wator</a><br>Contains <a href=\"https://pypi.python.org/pypi/PyQt5/5.9.1\">PyQt5</a> and graphics from <a href=\"opengameart.org\">OpenGameArt.org</a>")
    return

