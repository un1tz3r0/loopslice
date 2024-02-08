from setuptools import setup

setup(
    name='loopslice',
    version='0.1.0',
    py_modules=['loopslice'],
    install_requires=[
        'Click',
        'git+https://github.com/CPJKU/madmom',
        'pydub'
    ],
    entry_points={
        'console_scripts': [
            'loopslice = loopslice:cli',
        ],
    },
)
