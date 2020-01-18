import setuptools

from pyastar.version import __version__

# ---------------------------------------------------------------------------------------------------------
# GENERAL
# ---------------------------------------------------------------------------------------------------------


__name__ = "pyastar"
__author__ = "Julian Blank"
__url__ = "https://www.egr.msu.edu/coinlab/pyastar/"

data = dict(
    name=__name__,
    version=__version__,
    author=__author__,
    url=__url__,
    python_requires='>=3.6',
    author_email="blankjul@egr.msu.edu",
    description="AStar Algorithm",
    license='Apache License 2.0',
    keywords="graph, heuristic search",
    install_requires=[],
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics'
    ]
)


# ---------------------------------------------------------------------------------------------------------
# METADATA
# ---------------------------------------------------------------------------------------------------------


# update the readme.rst to be part of setup
def readme():
    with open('README.rst') as f:
        return f.read()


def packages():
    return ["pyastar"] + ["pyastar." + e for e in setuptools.find_packages(where='pyastar')]


data['long_description'] = readme()
data['packages'] = packages()

setuptools.setup(**data)
