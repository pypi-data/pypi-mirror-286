# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/

from setuptools import setup

setup(name='Approximation',
      version='1.0.0',
      description='This package is created to approximate distributions',
      packages=['Approximation'],
      author='Taha Huzeyfe Aktas',
      author_email='taha.huzeyfe@gmail.com',
      install_requires=['scipy', 'math'],
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
      zip_safe=False)