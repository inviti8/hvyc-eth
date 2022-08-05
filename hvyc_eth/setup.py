#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    author="Meta Cronos",
    author_email='comicronos@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Heavy Meta ethereum smart contract handling.",
    entry_points={
        'console_scripts': [
            'hvyc_eth=hvyc_eth.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='hvyc_eth',
    name='hvyc_eth',
    packages=find_packages(include=['hvyc_eth', 'hvyc_eth.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/inviti8/hvyc_eth',
    version='0.0.0',
    zip_safe=False,
)
