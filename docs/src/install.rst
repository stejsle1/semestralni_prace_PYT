Install
=======

How to install module WaTor
---------------------------

Wator application is install as Python module. Module can be downloaded from GitHub repository ``https://github.com/stejsle1/semestralni_prace_PYT/releses`` as latest release.

After you download it you can install it.

Move to filder with extract files. To download all required modules run:

.. code:: Python

  python -m pip install -r requirements.txt
  
To make a module from file run:

.. code:: Python

  python setup.py develop

This command will automatically install required modules.

Now the Wator application is install and you can run application:

.. code:: Python

  python -m wator

To run functions of Wator without GUI you can just import a module:

.. code:: Python

  import wator

  ...

For details about configuration of GUI see :ref:`config-manual`.
