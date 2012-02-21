"""
It's almost impossible to get an install that works automatically for this test.
However, this gets you pretty fat

Ad-hoc customisations: 

 * bottle-redis needs a connection pool (see my pull request #11) 
 * bottle.py patched to supress gevent's wsgi server logging 
 * pypy needs to disable twisted's extensions when installing

gevent should be 1.0 beta. 

"""
from setuptools import setup
import sys

is_pypy = hasattr(sys, 'pypy_version_info')

extras = []
if not is_pypy: 
   extras.extend(['gevent>1.0b1', 'cython'])

setup(
        name='webbench',
        version='0.0.1',
        install_requires=['tornado', 'twisted', 'cyclone',
            'flask', 'bottle', 'bottle-redis', 'redis',
            'rocket', 'paste'
            ] + extras,
)

