#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


def load_requirements(fname):
    with open(fname) as f:
        return f.read().strip().split('\n')


requirements = load_requirements("requirements.txt")

setup_requirements = []

test_requirements = load_requirements("requirements_test.txt")

dev_requirements = test_requirements\
                   + load_requirements("requirements_dev.txt")

setup(
    author="Ian Williams",
    author_email='ian.williams@netspi.com',
    python_requires='>=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A utility to convert your AWS CLI credentials into AWS "
                "console access.",
    entry_points={
        'console_scripts': [
            'aws_consoler=aws_consoler.cli:main',
        ],
    },
    extras_require={
        "dev": dev_requirements,
        "test": test_requirements
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='aws_consoler',
    name='aws_consoler',
    packages=find_packages(include=['aws_consoler', 'aws_consoler.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/netspi/aws_consoler',
    version='1.1.0',
    zip_safe=True,
)
