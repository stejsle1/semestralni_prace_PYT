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
    return y // CELL_SIZE, x // CELL_SIZE


def logical_to_pixel(row, column):
    return column * CELL_SIZE, row * CELL_SIZE



class GridWidget(QtWidgets.QWidget):
    def __init__(self, array, energy):
        super().__init__()  # musime zavolat konstruktor predka
        self.array = array
        self.energy = energy
        self.stop = False
        self.opti = 1

        # nastavime velikost podle velikosti matice, jinak je nas widget prilis maly
        size = logical_to_pixel(*array.shape)
        self.setMinimumSize(*size)
        self.setMaximumSize(*size)
        self.resize(*size)

    def mousePressEvent(self, event):
        # prevedeme klik na souradnice matice
        row, column = pixel_to_logical(event.x(), event.y())

        # Pokud jsme v matici, aktualizujeme data
        if 0 <= row < self.array.shape[0] and 0 <= column < self.array.shape[1]:
            self.array[row, column] = self.selected
            if self.selected < 0:
               self.energy[row, column] = self.initEnergy

            # timto zajistime prekresleni widgetu v miste zmeny:
            # (pro Python 3.4 a nizsi volejte jen self.update() bez argumentu)
            self.update(*logical_to_pixel(row, column), CELL_SIZE, CELL_SIZE)

    # vzdycky, kdyz je treba neco prekreslit, kdyz je treba, reaguje na udalost
    # metoda, protoze nejde pouzit v connect(slot)
    def paintEvent(self, event):
        rect = event.rect()  # ziskame informace o prekreslovane oblasti

        # zjistime, jakou oblast nasi matice to predstavuje
        # nesmime se pritom dostat z matice ven
        row_min, col_min = pixel_to_logical(rect.left(), rect.top())
        row_min = max(row_min, 0)
        col_min = max(col_min, 0)
        row_max, col_max = pixel_to_logical(rect.right(), rect.bottom())
        row_max = min(row_max + 1, self.array.shape[0])
        col_max = min(col_max + 1, self.array.shape[1])

        painter = QtGui.QPainter(self)  # budeme kreslit

        for row in range(row_min, row_max):
            for column in range(col_min, col_max):
                # ziskame ctverecek, ktery budeme vybarvovat
                x, y = logical_to_pixel(row, column)
                rect = QtCore.QRectF(x, y, CELL_SIZE, CELL_SIZE)

                #BARVY
                # seda pro zdi, zelena pro travu
                #if self.array[row, column] < 0:
                #    color = QtGui.QColor(115, 115, 115)
                #else:
                #    color = QtGui.QColor(0, 255, 0)

                # OBRAZKY
                # podkladova barva pod polopruhledne obrazky
                white = QtGui.QColor(255, 255, 255)
                painter.fillRect(rect, QtGui.QBrush(white))

                # travu dame vsude, protoze i zdi stoji na trave
                SVG_WATER.render(painter, rect)

                # zdi dame jen tam, kam patri
                if self.array[row, column] > 0:
                    SVG_FISH.render(painter, rect)
                if self.array[row, column] < 0:
                    SVG_SHARK.render(painter, rect)

                # vyplnime ctverecek barvou
                #painter.fillRect(rect, QtGui.QBrush(color))


