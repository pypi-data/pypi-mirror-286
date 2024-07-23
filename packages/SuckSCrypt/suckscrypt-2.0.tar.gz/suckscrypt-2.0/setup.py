from setuptools import setup, find_packages

setup(
    name='SuckSCrypt',
    version='2.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pycryptodome',
        'pyarmor'
    ],
    description='A Fastest & Secure Encryption System.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='KyzuneX',
    author_email='kyzunex@gmail.com',
    url='https://github.com/IT-Club-SMKN-21-Jakarta/SuckSCrypt',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)