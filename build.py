import os

# See if Cython is installed
try:
     from Cython.Build import cythonize
     # Do nothing if Cython is not available
except ImportError:
     # Got to provide this function. Otherwise, poetry will fail
     def build(setup_kwargs):
          pass
# Cython is installed. Compile
else:
     from setuptools import Extension
     from distutils.command.build_ext import build_ext
     import numpy as np

     
     # This function will be executed in setup.py:
     def build(setup_kwargs):
         
          dir = "ektelo/algorithm/privBayes/"
          
          sources = ["privBayesSelect.pyx", 
           "lib/methods.cpp",
           "lib/table.cpp", 
           "lib/translator.cpp", 
           "lib/noise.cpp",
           "lib/privBayes_model.cpp"]

          # gcc arguments hack: enable optimizations
          os.environ['CFLAGS'] = '-O3'

          # Build
          setup_kwargs.update({
               'ext_modules': cythonize(Extension(
                "ektelo.privBayesSelect",                           # the extension name
               sources=[dir + s for s in sources],            # the Cython source and
                                                  # additional C++ source files
               language="c++",                        # generate and compile C++ code
               extra_compile_args=["-std=c++11"],
               extra_link_args=["-std=c++11"],
               include_dirs=[np.get_include()]
               )),
               'cmdclass': {'build_ext': build_ext}
          })