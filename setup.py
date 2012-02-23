"""
It's almost impossible to get an install that works automatically for this test.
However, this gets you pretty fat

Ad-hoc customisations: 

 * bottle-redis needs a connection pool (see my pull request #11) 
 * pypy needs to disable twisted's extensions when installing
 * eventlet: pypy needs --without-greenlet 

gevent should be 1.0 beta. 

"""
from setuptools import setup
import sys

is_pypy = hasattr(sys, 'pypy_version_info')

extras = []
if not is_pypy: 
   extras.extend(['eventlet', 'cython'])

setup(
        name='webbench',
        version='0.0.1',
        install_requires=['tornado', 'twisted', 'cyclone',
            'flask', 'bottle', 'bottle-redis', 'redis',
            'rocket', 'paste', 'pyramid', 'eventlet'
            ] + extras,
)

