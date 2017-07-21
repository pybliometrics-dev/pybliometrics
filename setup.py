from setuptools import setup

setup(name='scopus',
      version='0.2.1',
      description='Python API for Scopus',
      url='http://github.com/scopus-api/scopus',
      author='John Kitchin and Michael E. Rose',
      author_email='jkitchin@andrew.cmu.edu or Michael.Ernst.Rose@gmail.com',
      license='MIT',
      packages=['scopus', 'scopus.utils'],
      scripts=['scopus/bin/scopus_coauthors'],
      test_suite = 'nose.collector',
      long_description='''Provides Python functions to retrieve data from the Scopus APIs.''',
      install_requires=['nose'])
