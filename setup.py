from setuptools import setup

setup(
        name='webbench',
        version='0.0.1',
        install_requires=['tornado', 'twisted', 'cyclone',
            'flask', 'bottle', 'bottle-redis', 'redis',
            'rocket', 'paste'
            ],
)

