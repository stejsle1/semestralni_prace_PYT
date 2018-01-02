.. _config-manual:

CONFIG
======

Configuration can be set only by managging array of creatures. This can be set by openning and saving file with this array in GUI application.

Simulation configuration
------------------------

On right side of window there are 4 fields and 1 slider to set variables for simulation.

User can set *age_fish*, *age_shark*, *energy_initial* and *energy_eat* (more information in :ref:`use-manual` or :ref:`api-label`). Last settings variable is *optimalize percentage* - it set amount of creatures, which will be add in optimalize simulation.

This settings can be change while simulation running on.

Configuration by files
----------------------

Open configuration
~~~~~~~~~~~~~~~~~~

To open file with saved array of creatures click to button ``'Open'`` in menu ``'File'``. Application will read special format in file and create array with creatures on same position they was before saving. 

Save configuration
~~~~~~~~~~~~~~~~~~

To save file with array of creatures click to button ``'Save'`` in menu ``'File'``. Application save this array in special format readable be this application. 

Optimized configuration
~~~~~~~~~~~~~~~~~~~~~~~

User can open configuration which has high chance to run in infinite loop without optimalization (adding creatures if species die off). This simulation is named ``'optimized_configuration'``. This configuration cannot guarantee that simulation will run in infinite loop.
