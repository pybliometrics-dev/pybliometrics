from setuptools import setup

setup(name = 'scopus',
      version='0.1',
      description='Python API for Scopus',
      url='http://github.com/jkitchin/scopus',
      author='John Kitchin',
      author_email='jkitchin@andrew.cmu.edu',
      license='GPL',
      packages=['scopus'],
      scripts=['scopus/bin/scopus_coauthors'],
      test_suite = 'nose.collector',
      long_description='''Provides Python functions to retrieve data from the Scopus APIs.''',
      install_requires=[
          'nose'],)


# to setup user on pypi
# python setup.py register
# to push to pypi - python setup.py sdist upload
