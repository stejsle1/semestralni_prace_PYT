.. _gui-manual:

GUI
===

If WaTor module is :ref:`installed<install-label>` you can start to use it.

This page will show you how to use GUI of application. To see how use modul withou GUI see :ref:`use-manual`.

To use WaTor GUI run command:

.. code:: Python

  python -m wator
  
It opens new window with GUI of WaTor.

Layout
------

Main window of WaTor application is divided into 4 sections. First main section is window which shows animated array of creatures and options while starting program. 

Second section - rectangle above main window - prints graph showing actual amount of creatures. 

Third section is settings on right side of window. In upper part of section is settings for simulations. In bottom part there are icons of water, fish and shark - user can add creatures or remove them by adding water.

Fourth section is the most upper side - menu. In menu there is **File**, **Action*** and **Help**. In **File** menu user can save or open array of creatures, create new one or close application. In **Action** menu user can move to next chronon or run simulations (basic or optimalize). In **Help** menu user can open **'About'** page. Also there are buttons as shotcut for buttons in menu.

Next chronon
------------

Button *Next chronon* run *tick* function once.  

Simulation
----------

Simulation is an infinite loop of running *tick* function.

Simulation can be run by clicking on *Simulation* button and stopped by clicking on *Stop* button. 

This simulation run until one of species die or until user click on *Stop* button. 

Optimalize simulation
---------------------

Simulation is an infinite loop of running *tick* and *optimalize* functions in pairs - makes equilibrium constantly. 

Simulation can be run by clicking on *Opti simulation* button and stopped by clicking on *Stop* button. 

This simulation automatically add some creatures if it decides one of species will die. It means that simulation never ends - never can happen a case that species die off. 

Settings
--------

On right side of window there are 3 fields and 1 slider to set variables for simulation.

User can set *age_fish*, *age_shark* and *energy_eat* (more information in :ref:`use-manual` or :ref:`api-label`). Last settings variable is *optimalize percentage* - it set amount of creatures, which will be add in optimalize simulation.

This settings can be change while simulation running on. 

Create array of creatures
-------------------------

In bottom part of right side there is list of icons. They are symbols of water, fish and shark. To create new array user can choose and click on icon and then add these items to array by clicking on array spaces. To delete creature from array just reclick on space with water icon.

Graph field
-----------

On upper part of main window is rectangle with graph. This graph showing actual amount of fish and sharks and amount of added fish and sharks while optimalizing. Red color means fish part, blue color means shakrs part. Lines are actual amount of creatures, dots are amount of creatures added to simulation.