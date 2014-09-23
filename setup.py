from setuptools import setup, find_packages


# Dynamically calculate the version based on pymal.VERSION.
version = __import__('reloaded_set').__version__


setup(
    name='reloaded-set',
    packages=find_packages(exclude=['tests*']),
    version=version,
    description='A python api for the website MyAnimeList (or MAL).',
    author='pymal-developers',
    license="BSD",
    url='https://bitbucket.org/pymal-developers/pymal/',
    keywords=['reloaded', 'set', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
