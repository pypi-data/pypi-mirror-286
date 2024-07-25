from setuptools import setup, find_packages

VERSION = '0.0.2024072409'
DESCRIPTION = 'bighummingbird'

with open('requirements.txt') as f:
    required = f.read().splitlines()

# Setting up
setup(
    name="bighummingbird",
    version=VERSION,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=required,

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
