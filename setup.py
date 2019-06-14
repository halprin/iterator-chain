from setuptools import setup, find_packages
from iterator_chain import __version__

with open('README.md', 'r') as read_me:
    long_description = read_me.read()

setup(
    name='iterator-chain',
    version=__version__,
    author='halprin',
    author_email='me@halprin.io',
    description='Chain together lazily computed modifications to iterators',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/halprin/iterator-chain',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(exclude='tests'),
    install_requires=[]
)
