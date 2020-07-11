from setuptools import setup, find_packages

setup(
    name='tapuzim',
    version='1.0.0',
    author='Tomer Mardan',
    packages=find_packages(),
    install_requires=['flask', 'flask-cors'],
)
