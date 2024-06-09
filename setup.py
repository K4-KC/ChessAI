from distutils.core import setup, Extension

module1 = Extension('chess', sources = ['tst.cpp'])

setup (name = 'chess',
       version = '1.0',
       description = 'This is a chess module in C',
       ext_modules = [module1])