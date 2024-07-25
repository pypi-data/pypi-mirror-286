# setup.py
from setuptools import setup, find_packages

setup(
    name='DataNinja',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'missingno',
        'ydata-profiling'
    ],
    author='Nicolas Prieur',
    author_email='pu-zle@live.fr',
    description='A comprehensive data analysis and visualization toolkit.',
    url='https://github.com/ShelbyTO/DataNinja'
)
