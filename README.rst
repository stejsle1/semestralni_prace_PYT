WaTor
=====

This is a application with graphical user interface (GUI). This project is about WaTor - WaTor is simulation of sea world with fish and sharks (predator/prey). This project follow up on project WaTor (``https://github.com/stejsle1/wator``).


Install
-------

Wator application is install as Python module. Module can be downloaded from GitHub repository ``https:://github.com/stejsle1/semestralni_prace_PYT``. 

After you downloaded it you can install it.

Move to folder with extract files. To install requirements run:

.. code:: Python

   python -m pip install -r requirements.txt

To make a module from file run:

.. code:: Python

   python setup.py develop
 
This command will automatically install required modules.

 
GUI
---

WaTor allow to run application with graphical user interface (GUI). 

To run GUI type:

.. code:: Python

    python -m wator


GUI allow to save and open simulation or create new one - all by clicking on ``'File'`` menu and picking one of listed buttons.
Button ``'Next chronon'`` run function *tick()*, button ``'Simulation'`` run function *tick()* in infinite loop (stoppable by button 'Stop' or by extinction one of species). Button ``'Optimalized simulation'`` run same as ``'Simulation'``, but if one of species start to die off application add a few creatures to establish an equilibrium.
Button ``'About'`` in menu ``'Help'`` print out a window with information about application.
Button ``'Quit'`` exits the application.

Documentation
-------------

Documentation is save in ``docs`` folder in module. Before running command to make documentation run command to install all required packages:

.. code:: Python

  python -m pip install -r docs/requirements.txt

To set documentation into HTML format run:

.. code:: Python

  cd docs
  make html

Now in ``docs/_build/html/`` folder in placed file ``'index.html'`` with documentation.

Documentation also contains tests. Tests can be checked by running command:

.. code:: Python

  make doctest


License
-------

This project is licensed under the CCO License - see LICENSE file for more information.
