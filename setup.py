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

