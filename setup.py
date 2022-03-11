from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='mdetector',
    version='1.0',
    packages=find_packages(),
    py_modules=['mdetector'],
    package_dir={'mdetector': 'mdetector'},
)