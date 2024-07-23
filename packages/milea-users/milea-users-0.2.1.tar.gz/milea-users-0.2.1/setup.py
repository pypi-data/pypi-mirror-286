
from setuptools import find_packages, setup

setup(
    name='milea-users',
    version='0.2.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['milea_base>=0.1'],
    author='red-pepper-services',
    author_email='pypi@schiegg.at',
    description='Milea Framework - Milea Users Module',
    license='MIT',
)
