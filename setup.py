'''
Setup.py for arff

First time ever on pypi use:
    setup.py sdist register upload

'''


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path
import sys


import arff
DOCUMENTATION = arff.__doc__

VERSION = '0.8'

SETUP_DICT = dict(
    name='arff',
    packages=['arff'],
    version=VERSION,
    author='ubershmekel',
    author_email='ubershmekel@gmail.com',
    url='http://code.google.com/p/arff/',
    description='Python package for reading and writing Weka arff files',
    long_description=DOCUMENTATION,
    test_suite='arff.test.test_arff',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
  )

try:
    # Allows uploading the source dist to google code
    from googlecode_distutils_upload import upload
    CMD_CLASS = {'google_upload': upload}
    SETUP_DICT['cmdclass'] = CMD_CLASS
except Exception:
    pass

# generate .rst file with documentation
#open(os.path.join(os.path.dirname(__file__), 'documentation.rst'), 'w').write(DOCUMENTATION)

setup(**SETUP_DICT)
