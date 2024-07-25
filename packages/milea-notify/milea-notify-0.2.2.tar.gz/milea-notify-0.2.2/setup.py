
from setuptools import find_packages, setup

setup(
    name='milea-notify',
    version='0.2.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['milea_base>=0.4.2'],
    author='red-pepper-services',
    author_email='pypi@schiegg.at',
    description='Milea Framework - Milea Notify Module',
    license='MIT',
)
