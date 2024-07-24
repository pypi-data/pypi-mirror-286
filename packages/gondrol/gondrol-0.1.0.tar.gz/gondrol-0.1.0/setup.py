from setuptools import setup, find_packages

VERSION = '0.1.0'


# Setting up
setup(

    # Name of the package
    name="gondrol",

    # Start with a small number and increase it with every change you make
    # https://semver.org
    version=VERSION,

    # Author information
    author="Andri Ariyanto",
    author_email="ariyant.andri@gmail.com",

    # Short description of your library
    description="My Personal Python Packages",

    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    
    # List of keyword arguments
    keywords=['python', 'gondrol'],

    # Packages to include into the distribution
    packages=find_packages(),

    # List of packages to install with this one
    install_requires=[],

    # https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)