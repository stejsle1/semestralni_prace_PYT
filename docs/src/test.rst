.. _test-manual:

TEST
====

Documentation can test some **wator** function to see how they works. To see how to run tests on own machine see :ref:`last capture<test-machine>`.

.. testsetup::

   
   from wator import WaTor
   import numpy
   creatures = numpy.zeros((8, 8))
   creatures[2, 4] = 3
   creatures[1, :] = -5
   energies = numpy.zeros((8, 8))
   energies[1, :] = 3

Init
----

Basic instance of WaTor is created with prepared array of numbers:

.. doctest::

   >>> wator = WaTor(creatures)
   

*Init* function doesn't return any value, but user can make sure that the instance was created by testing an array of creatures:

.. testcode::

   wator = WaTor(creatures)
   print(wator.creatures)

.. testoutput::

   [[ 0.  0.  0.  0.  0.  0.  0.  0.]
    [-5. -5. -5. -5. -5. -5. -5. -5.]
    [ 0.  0.  0.  0.  3.  0.  0.  0.]
    [ 0.  0.  0.  0.  0.  0.  0.  0.]
    [ 0.  0.  0.  0.  0.  0.  0.  0.]
    [ 0.  0.  0.  0.  0.  0.  0.  0.]
    [ 0.  0.  0.  0.  0.  0.  0.  0.]
    [ 0.  0.  0.  0.  0.  0.  0.  0.]]

Next example shows how to make instance with random placed creatures by setting shape, number of fish and number of sharks: 

.. doctest::

   >>> wator = WaTor(shape=(8, 8), nfish=16, nsharks=4)
   

User can set age of fish and shark, when creature will reproduce itself:   

.. doctest::

   >>> wator = WaTor(shape=(8, 8), nfish=16, nsharks=4, age_fish=5, age_shark=6)

                  
User can set initial energy - amount of energy sharks will get in begining, and energy from eating fish:   

.. doctest::

   >>> wator = WaTor(creatures, energy_initial=12, energy_eat=5)                 


Instance of WaTor can set prepared array of energies of sharks:

.. doctest::

   >>> wator = WaTor(creatures, energies=energies)                 
               

Tick function
-------------

Tick function of WaTor instance is running this way: ``wator.tick()``. Function return ``self`` of instance. To see *tick* function, let's print creatures array before and after *tick* function:   

.. testcode::

   creatures2 = numpy.zeros((2, 1))
   creatures2[0, 0] = 2
   wator = WaTor(creatures2)
   print(wator.creatures)
   print('------')
   wator.tick()
   print(wator.creatures)

.. testoutput::

   [[2.]
    [0.]]
   ------ 
   [[0.]
    [3.]]    
    
In first array fish lay in position [0, 0]. *Tick* function move it to only free position.                
  
  
Getters
-------

WaTor functions *count_fish* and *count_sharks* get actual count of fish:

.. testcode::

   wator = WaTor(creatures, energies=energies)
   print(wator.count_fish())

.. testoutput::

   1
   
and sharks:

.. testcode::

   wator = WaTor(creatures, energies=energies)
   print(wator.count_sharks())

.. testoutput::

   8   
   
Setters
-------

WaTor functions for settings are *setAge_fish*, *setAge_shark*, *setEnergy_eat* and *setOpti*. First one setting age of fish, when fish can reproduce itself:

.. testcode::

   print(wator.age_fish)
   wator.setAge_fish(12)
   print(wator.age_fish)

.. testoutput::

   5
   12
   
*SetAge_shark* sets a period when shark is capable of reproducing:

.. testcode::

   print(wator.age_shark)
   wator.setAge_shark(11)
   print(wator.age_shark)

.. testoutput::

   10
   11

*SetEnergy_eat* sets an amount of energy shark gains after eating fish:

.. testcode::

   print(wator.energy_eat)
   wator.setEnergy_eat(15)
   print(wator.energy_eat)

.. testoutput::

   3
   15

*SetOpti* sets indicator how many creatures will be added to array of creatures:

.. testcode::

   print(wator.opti)
   wator.setOpti(80, 75)
   print(wator.opti)

.. testoutput::

   0
   61.0

Optimalize
----------

Function *optimalize* makes equilibrium between species. So if one of species die off, function add some creatures to make equilibrium. Function works with *opti* atribut. 

.. testcode::

   creatures = numpy.zeros((20, 20))
   creatures[0, :] = 1 # 20 fish
   creatures[9, :] = -1 
   creatures[12, :] = -1
   creatures[15, :] = -1 # 60 sharks
   wator = WaTor(creatures)
   wator.setOpti(wator.count_fish()+wator.count_sharks(), 42)
   lim_f, lim_s = wator.optimalize()
   print(str(lim_f) + " fish and " + str(lim_s) + " sharks")

.. testoutput::

   14 fish and 0 sharks 


.. _test-machine:

Tests on machine
----------------

Tests for *wator* are placed in **wator_tests** directory. To run tests type:

.. code:: Python

   python -m pytest wator_tests/tests/*
  
This command run tests for testing *WaTor* module, not GUI of *wator*.

   
