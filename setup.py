from distutils.core import setup
from setuptools import find_packages

with open("README.md") as f:
    long_description = f.read()

setup(name='pddl-plus-parser',
      version='3.3.13',
      python_requires=">=3.8",
      description='Parser of PDDL+ domains and problems for learning purposes',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Argaman Mordoch',
      packages=find_packages(exclude=["tests"])
     )