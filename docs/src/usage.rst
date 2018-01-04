.. _use-manual:

USAGE
=====

If WaTor module is :ref:`installed<install-label>` you can start to use it.

This page will show you how to use module withou GUI. To see usage of GUI side of application see :ref:`gui-manual`.

To use WaTor module just import module to your script:

.. code:: Python

  import wator
  
  ...
  
Wator init
-----------------

To init WaTor instance type:

.. code:: Python 

  instance = WaTor(<init constant>)  

Every instance need to be created with knowing *size of array and number of creatures* to create or knowing *whole array of creatures*:

.. code:: Python 

  # case: size of array and number of creatures
  size_of_array = (15,15)
  instance = WaTor(shape=size_of_array, nfish=10, nsharks=6)
  
  #case: array of creatures
  creatures_array = numpy.zeros((15,15)) 
  creatures_array[0,2] = 1
  creatures_array[5,5] = -3
  instance = WaTor(creatures=creatures_array) 
  
*shape* stores size of array, *nfish* set number f fish in array and *nsharks* set number of shark in array. Init create array with size of *shape* and randomly place creatures in array. *Positive* number is for **fish**, *negative* number is for **shark**. *Absolute value* of that number is *age of creature*.     

This init has additional variables. You can set *array of energies* of sharks:

.. code:: Python

  energies_array = numpy.zeros((15,15)) 
  energies_array[5,5] = 2
  instance = WaTor(..., energies=energies_array)
  
Last additional variables are age_fish, age_shark, energy_eat and energy_initial. *age_fish* set age when fish is old enough to reproduce itself. *age_shark* set age when shark is old enough to reproduce itself. *energy_eat* set amount of energy that shark gains after eating a fish. *energy_initial* set amount of energy that shark gets on start/after breed. 

.. code:: Python

  instance = WaTor(..., age_fish=5, age_shark=10, energy_eat=3, energy_initial=0)
  
This init set array of creatures or energies and set its constants for further use. Instance then has own global variables which are accessible by typing:

.. code:: Python

  instance = WaTor(...)
  instance.creatures[0,4] = 1
  instance.energies[0,0] = 0
  instance.age_fish = 7
  instance.age_shark = 7
  

Tick function
-------------

This function makes one chronon - move fish, move sharks and decrease energies (so some sharks maybe die - delete dead sharks from array). Function can be run by:

.. code:: Python

  instance.tick()
  
*tick* function works with random function on moving creatures. Random function tell if creature will move to right, left, up or down (if there is a free space). First fish moves. Second sharks move - their priority is to move to fish space so they can eat them. If around them is no fish they move to free space as fish in previous phase. If there is n free sace to move (for fish or for shark) they stay at position. 

In first and second phase if creature achieve an age to breed a descendant they don't move but they breed to free space. Also if there is no empty space they wait for next chronon and try again. 

Last phase function decrese array with energies and find out if there is any dead shark (and it delete his position from array of creatures). 

Count_fish function
-------------------

This function returns actual number of fish in array.


Count_sharks function
---------------------

This function returns actual number of sharks in array.


Optimalize function
-------------------

This function works with function *tick*. After function *tick* makes one chronon, function *optimalize* looks to array of creatures and decide if there is enough creatures to run next chronon. If one of species seems to die off it add some creatures to array to make equilibrium. 

SetAge_fish function
--------------------

This function sets new age of fish.
   
SetAge_shark function
---------------------

This function sets age of sharks.

SetEnergy_eat function
----------------------

This function sets amount of energy adding after eating fish.

SetOpti function
----------------

This function sets amount of creatures adding in optimalize simulation.


For more information about API see :ref:`api-label`.