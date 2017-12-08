"""Setup file for dmux."""
from setuptools import setup, find_packages
with open('README.md') as f:
    README = f.read()
with open('LICENSE') as f:
    LICENSE = f.read()
with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()
setup(
    name='dmux',
    version='0.1.0',
    description='A simple script for running processes/services inside of tmux',
    long_description=README,
    author='Eugene Kovalev',
    author_email='euge.kovalev@gmail.com',
    url='https://github.com/Abraxos/dmux',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=REQUIREMENTS,
    entry_points={'console_scripts': ['dmux = dmux.dmux:dmux']}
)
