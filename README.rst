============
AWS Consoler
============


.. image:: https://img.shields.io/pypi/v/aws_consoler.svg
        :target: https://pypi.python.org/pypi/aws_consoler

.. image:: https://img.shields.io/github/workflow/status/netspi/aws_consoler/Build%20package
        :target: https://github.com/NetSPI/aws_consoler/actions

.. image:: https://readthedocs.org/projects/aws-consoler/badge/?version=latest
        :target: https://aws-consoler.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


A utility to convert your AWS CLI credentials into AWS console access.


* Free software: BSD License
* Documentation: https://aws-consoler.readthedocs.io.


Features
--------

* Load credentials from the command line or from boto3 sources (envvars, profiles, IMDS)
* Coordinate communication to AWS Federation endpoint
* Select appropriate endpoint based on partition
* Load resultant URL in user's browser of choice

Credits
-------

Thanks to some of the bloggers at AWS (Jeff Barr, Kai Zhao) for the helpful guides on Federation in AWS.

Thanks to Karl Fosaaen (@kfosaaen) for the inspiration to write this tool.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
