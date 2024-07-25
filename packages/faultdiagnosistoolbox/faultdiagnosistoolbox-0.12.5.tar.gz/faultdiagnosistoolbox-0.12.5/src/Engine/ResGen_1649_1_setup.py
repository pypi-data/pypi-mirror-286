# Build file for compiling ResGen_1649_1.c
#
# Compile by executing:
# > python ResGen_1649_1_setup.py build
# at a shell prompt

# File generated Thu Jul 18 15:25:19 2024

from setuptools import setup, Extension
import numpy as np

incdir = np.get_include()

module1 = Extension('ResGen_1649_1',
                    sources=['ResGen_1649_1.cc', 'extmodelfuns.cc'],
                    include_dirs=[incdir],
                    extra_compile_args=['-Wno-unused-function'])

setup(name='ResGen_1649_1',
      version='0.1',
      description='Module for residual generator ResGen_1649_1',
      ext_modules=[module1])
