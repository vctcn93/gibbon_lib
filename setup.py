from setuptools import setup, find_packages
from setuptools.extension import Extension
import numpy as np

ext_modules = [
    Extension('pangolin/**/*', ['pangolin/**/*.pyx'], include_dirs=[np.get_include()])
]

packages = find_packages()
lc = open('LICENSE').read()
#rm = open('README.txt').read()

setup(
    name = "gibbon",
    version = "0.0.1",
    author = "vctcn93",
    author_email = "vincentvane@yeah.net",
    description = ("library required to perform architecture modeling and planning"),
    license = lc,
    include_dirs = [np.get_include()],
    packages=packages,
    #long_description=rm,
    install_requires=['numpy', 'pandas', 'pytest', 'networkx', 'flask', 'scipy', 'pillow',
                    'shapely'],
    zip_safe=False
)
