#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os

from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.command.develop import develop

import berset_engine
# ==============Package meta-data==============
NAME = 'berset_engine'
DESCRIPTION = 'Bulding Energy Retrofit Scenario Evaluation Tool Engine'
URL = 'https://github.com/longlevan/berset_engine'
EMAIL = 'long.le-van@outlook.com'
AUTHOR = 'Van Long Le'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = berset_engine.__version__
STATUS = "Underdevelopment"

# What packages are required for this module to be executed
REQUIRED = [
    'pandas>=2.0.0',
    'geocoder>=1.38.1',
    'ish_parser>=0.0.22',
    'numpy>=1.20.0',
    'scipy>=1.11.0',
    'xlrd>=2.0.1',
    'geopy>=2.4.1',
    'python-dotenv>=1.0.1',
    'plotly>=5.8.0',
    'Jinja2>=3.1.2',
    "python-dotenv>=1.0.1"
]

# What packages are optional
EXTRAS = {
    # 'plotly': ['plotly'],
}

here = os.path.abspath(os.path.dirname(__file__))

# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


# class PostInstallCommand(install):
#     """
#     Post-installation for installation mode
#     NOTE: Only works when installing a source distribution zip
#     or tarball, or installing in editable mode from a source tree.
#     It will not work when installing from a binary wheel (.whl)
#     """
#     @staticmethod
#     def status(s):
#         """Prints things in bold."""
#         print('\033[1m{0}\033[0m'.format(s))

#     def run(self):
#         install.run(self)
#         self.status("run config scripts")
#         os.system('berset-config')


# class PostDevelopCommand(develop):
#     @staticmethod
#     def status(s):
#         """Prints things in bold."""
#         print('\033[1m{0}\033[0m'.format(s))

#     def run(self):
#         develop.run(self)
#         self.status("run config scripts")
#         os.system('berset-config')


setup(
    name=NAME,
    version=about['__version__'],
    license='MIT',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(
        exclude=[
            "tests",
            "*.tests",
            "*.tests.*",
            "tests.*"
        ]
    ),
    # package_dir = {},
    # python_modules=[],
    package_data={"": ["*.cfg"]},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    project_urls={
        "Documentation": "https://github.com/longlevan/berset_engine/",
        "Changelog": (
            "https://github.com/longlevan/berset_engine/CHANGELOG.md"
        ),
        "Issue Tracker": "https://github.com/longlevan/berset_engine/issues",
    },
    keywords=[
        # eg: 'keyword1'
    ],
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    entry_points={
        # 'console_scripts': [
        #     'berset=berset_engine.interfaces.cli:main',
        # ],
    },
    # cmdclass={
    #     'install': PostInstallCommand,
    #     'develop': PostDevelopCommand
    # }
)
