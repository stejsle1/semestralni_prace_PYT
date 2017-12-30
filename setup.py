from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

with open('README.rst') as f:
    long_description = ''.join(f.readlines())


setup(
   name='wator-ultimate',
   version='0.1',
   keywords='wator simulation numpy fish shark sea',
   description='Python simulation of WaTor with GUI and autatic add of creatures',
   ext_modules=cythonize([Extension('wator.wator', ['wator/wator.pyx'],
                                   include_dirs=[numpy.get_include()])],
                                   language_level=3),
   include_dirs=[numpy.get_include()],
   install_requires=[
        'Cython',
        'NumPy',
        'pytest',
        'PyQt5',
        'matplotlib',
   ],
   long_description=long_description,
   author='Lenka Stejskalova',
   author_email='stejsle1@fit.cvut.cz',
   license='Public Domain',
   url='https://github.com/stejsle1/semetralni_prace_PYT',
   classifiers=[
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Console',
        ],
   zip_safe=False,
   packages=find_packages(), 
   entry_points={
      'console_scripts': [
          'wator = gui:main',
      ],
   },
)

