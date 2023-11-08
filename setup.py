from setuptools import setup

setup(
    name='loopsex',
    version='0.1.0',
    py_modules=['loopsex'],
    install_requires=[
        'Click',
        'git+https://github.com/CPJKU/madmom',
        'pydub'
    ],
    entry_points={
        'console_scripts': [
            'loopsex = loopsex:cli',
        ],
    },
)
