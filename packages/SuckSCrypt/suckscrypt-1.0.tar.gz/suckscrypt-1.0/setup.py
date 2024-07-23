# setup.py
from setuptools import setup, find_packages

setup(
    name='SuckSCrypt',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pycryptodome'
    ],
    description='A Fastest & Secure Encryption System.',
    author='KyzuneX',
    author_email='kyzunex@gmail.com',
    url='https://github.com/IT-Club-SMKN-21-Jakarta/SuckSCrypt',
)