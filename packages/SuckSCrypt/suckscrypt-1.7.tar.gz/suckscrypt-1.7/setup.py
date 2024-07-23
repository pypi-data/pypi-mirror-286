from setuptools import setup, find_packages

setup(
    name='SuckSCrypt',
    version='1.7',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pycryptodome'
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
    package_data={
        'suckscrypt': ['pyarmor_runtime_000000/pyarmor_runtime.pyd'],
    },
    python_requires='>=3.6',
)