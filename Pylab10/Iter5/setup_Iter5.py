from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("Iter_5.pyx", annotate=True),
)

