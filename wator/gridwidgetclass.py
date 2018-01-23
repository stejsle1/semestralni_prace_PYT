from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg, uic
import numpy
import time
import os.path
from wator import WaTor


CELL_SIZE = 32

SVG_WATER = QtSvg.QSvgRenderer('wator/gui/water.svg')
SVG_FISH = QtSvg.QSvgRenderer('wator/gui/fish.svg')
SVG_SHARK = QtSvg.QSvgRenderer('wator/gui/shark.svg')

VALUE_ROLE = QtCore.Qt.UserRole


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



class GridWidget(QtWidgets.QWidget):
    def __init__(self, array, energy):
        """
        Init GridWinget instance
        
        :param: ``array`` Array of creatures.
        :param: ``energy`` Array of energies.
        :return: ``None``
        """
        super().__init__()  # call constructor of ascensor
        self.array = array
        self.energy = energy
        self.stop = False
        self.opti = 1

        # set size according array size
        size = logical_to_pixel(*array.shape)
        self.setMinimumSize(*size)
        self.setMaximumSize(*size)
        self.resize(*size)
        self.filepath = "wator/gui/simulations/"

    def mousePressEvent(self, event):
        """
        Update arrays of creatures and energies after adding new creatures or water into main matrix.
        
        :param: ``event`` Clicked place.
        :return: ``None``
        """
        # convert click to logical cols and rows
        row, column = pixel_to_logical(event.x(), event.y())

        # if in array, update 
        if 0 <= row < self.array.shape[0] and 0 <= column < self.array.shape[1]:
            self.array[row, column] = self.selected
            if self.selected < 0:
               self.energy[row, column] = self.initEnergy

            # this ensure to rewrite widget:
            # (for Python 3.4 and below call self.update() without arguments)
            self.update(*logical_to_pixel(row, column), CELL_SIZE, CELL_SIZE)

    # when need to rewrite, react to event
    # method, because cant use in connect()
    def paintEvent(self, event): 
        """
        Rewrite updating place - fill place with picture.
        
        :param: ``event`` Clicked place.
        :return: ``None``
        """
        rect = event.rect()  # get info about rewriting place

        # get logical position
        row_min, col_min = pixel_to_logical(rect.left(), rect.top())
        row_min = max(row_min, 0)
        col_min = max(col_min, 0)
        row_max, col_max = pixel_to_logical(rect.right(), rect.bottom())
        row_max = min(row_max + 1, self.array.shape[0])
        col_max = min(col_max + 1, self.array.shape[1])

        painter = QtGui.QPainter(self)  # set a painter

        for row in range(row_min, row_max):
            for column in range(col_min, col_max):
                # get pixels to rewrite (repaint)
                x, y = logical_to_pixel(row, column)
                rect = QtCore.QRectF(x, y, CELL_SIZE, CELL_SIZE)

                # pictures
                # underlying color under semi-transparent images
                white = QtGui.QColor(255, 255, 255)
                painter.fillRect(rect, QtGui.QBrush(white))

                # water everywhere
                SVG_WATER.render(painter, rect)

                # fish and shark pictures to place, where they has to be
                if self.array[row, column] > 0:
                    SVG_FISH.render(painter, rect)
                if self.array[row, column] < 0:
                    SVG_SHARK.render(painter, rect)



