# Build file for compiling ResGen_4477_86.c
#
# Compile by executing:
# > python ResGen_4477_86_setup.py build
# at a shell prompt

# File generated Thu Jul 18 15:25:22 2024

from setuptools import setup, Extension
import numpy as np

incdir = np.get_include()

module1 = Extension('ResGen_4477_86',
                    sources=['ResGen_4477_86.cc', 'extmodelfuns.cc'],
                    include_dirs=[incdir],
                    extra_compile_args=['-Wno-unused-function'])

setup(name='ResGen_4477_86',
      version='0.1',
      description='Module for residual generator ResGen_4477_86',
      ext_modules=[module1])
