from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg, uic
import numpy
import time
import os.path
from wator import WaTor
from .gridwidgetclass import GridWidget
from .matplot import print_plot

def next_chronon(window, grid):
    """
    Turn simulation into next chronon, run 1 tick function.
    
    :param: ``window`` Main window of application.
    :param: ``grid`` Layout of window.
    :return: ``None`` 
    """
    wator = WaTor(creatures=grid.array, energies=grid.energy)

    age_fish = window.findChild(QtWidgets.QSpinBox, 'age_fishBox').value()
    age_shark = window.findChild(QtWidgets.QSpinBox, 'age_sharkBox').value()
    eat = window.findChild(QtWidgets.QSpinBox, 'energy_eatBox').value()


    wator.setAge_fish(age_fish)
    wator.setAge_shark(age_shark)
    wator.setEnergy_eat(eat)

    # Turn to next chronon
    wator.tick()
    grid.array = wator.creatures
    grid.energy = wator.energies

    grid.update()



def simulation_loop(window, grid, app):
    """Run simulation of tick in loop.

    Can be stopped by button Stop or by case that every creatures die off.
    
    :param: ``window`` Main window of application.
    :param: ``grid`` Layout of window.
    :param: ``app`` Application.
    :return: ``None`` 
    """
     
    # Delete only content of file - data of previous simulation
    with open('wator/gui/simulations/logmatplot.txt', "w"):
        pass
        
    wator = WaTor(creatures=grid.array, energies=grid.energy)

    # User options are set in begining, not while simulating
    age_fish = window.findChild(QtWidgets.QSpinBox, 'age_fishBox').value()
    age_shark = window.findChild(QtWidgets.QSpinBox, 'age_sharkBox').value()
    eat = window.findChild(QtWidgets.QSpinBox, 'energy_eatBox').value()

    wator.setAge_fish(age_fish)
    wator.setAge_shark(age_shark)
    wator.setEnergy_eat(eat)

    def stop(self):
       self.stop = True

    action = window.findChild(QtWidgets.QAction, 'actionStop')
    action.triggered.connect(lambda: stop(grid))

    while True:

       # Break to Stop button
       if grid.stop == True:
          break

       # Turn to next chronon
       wator.tick()
       if wator.count_fish() == 0 and wator.count_sharks() == 0:
          break

       grid.array = wator.creatures
       grid.energy = wator.energies

       grid.update()
       time.sleep(0.5)
       app.processEvents()

    grid.stop = False


def simulation_opti(window, grid, app):
    """Run simulation of tick in loop and in same time control if one of kind of creatures doesn't die.

    In case one kind of creatures slowly die off it add some creatures to simulation to make equilibrium.

    Number of added creatures is sum of creatures in init state multiply by percentage set by user.

    Simulation can be stopped only by button Stop.
    
    :param: ``window`` Main window of application.
    :param: ``grid`` Layout of window.
    :param: ``app`` Application.
    :return: ``None`` 
    """
    
    # Delete only content of file - data of previous simulation
    with open('wator/gui/simulations/logmatplot.txt', "w"):
        pass
        
    wator = WaTor(creatures=grid.array, energies=grid.energy)
    sum = wator.count_fish() + wator.count_sharks()

    def stop(self):
       self.stop = True

    action = window.findChild(QtWidgets.QAction, 'actionStop')
    action.triggered.connect(lambda: stop(grid))


    while True:

       # break to Stop button
       if grid.stop == True:
          break

       # In every round of simulation read users options
       age_fish = window.findChild(QtWidgets.QSpinBox, 'age_fishBox').value()
       age_shark = window.findChild(QtWidgets.QSpinBox, 'age_sharkBox').value()
       eat = window.findChild(QtWidgets.QSpinBox, 'energy_eatBox').value()
       opti = window.findChild(QtWidgets.QSlider, 'opti_slider').value()

       wator.setAge_fish(age_fish)
       wator.setAge_shark(age_shark)
       wator.setEnergy_eat(eat)
       wator.setOpti(sum, opti)
       print(wator.opti)
       
       # Optimalize actual wator instance
       limit_fish, limit_shark = wator.optimalize()

       # Turn to next chronon
       wator.tick()
       
       # Print data into file
       log_for_matplot(wator.count_fish(), wator.count_sharks(), limit_fish, limit_shark)
       
       # Print graph from data
       print_plot()
    
       grid.array = wator.creatures
       grid.energy = wator.energies

       grid.update()
       time.sleep(0.5)
       app.processEvents()

    grid.stop = False


def log_for_matplot(nfish, nsharks, addfish, addsharks):
     """
     Save amount of creatures to file - log.
    
     :param: ``nfish`` Actual number of fish. 
     :param: ``nsharks`` Actual number of sharks. 
     :param: ``addfish`` Number of added fish.  
     :param: ``addsharks`` Number of added shark. 
     """

     # Send to matplot
     with open('wator/gui/simulations/logmatplot.txt', 'r+') as f:
         buffer1 = deque(f, maxlen=30)
     buffer1.append(str(nfish) + " " + str(nsharks) + " " + str(addfish) + " " + str(addsharks) + "\n")
     with open('wator/gui/simulations/logmatplot.txt', 'w+') as f:
         f.writelines(buffer1)