httpAWS: a CLI, cURL-like tool for AWS Services
###############################################

httpAWS is a command line HTTP client for AWS services. Its goal is to make CLI interaction with AWS web services as
human-friendly as possible. It provides a simple ``httpaws`` command that allows for sending HTTP requests to AWS
services using a simple and natural syntax, and displays colorized output. httpAWS can be used for testing, debugging,
and generally interacting direly with AWS services with HTTP requests.

httpAWS directly makes HTTP calls to AWS service endpoints using the `requests <http://docs.python-requests.org>`_ and
`aws-requests-auth <https://github.com/DavidMuller/aws-requests-auth>`_ modules.

This is a low-level command-line tool intended for use by developers so that they can easily make direct HTTP calls
to AWS services.  It is effectively a command-line programmatic replacement for using a graphical tool like
`Postman <https://www.getpostman.com>`_ and was inspired by tools like `HTTPie <https://httpie.org>`_ but is specific to
AWS services.

.. class:: no-web no-pdf

|pypi|

.. |pypi| image:: https://img.shields.io/pypi/v/httpaws.svg?style=flat-square&label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/httpaws
    :alt: Latest version released on PyPi

.. contents::

.. section-numbering::

Main features
=============

* Expressive and intuitive syntax
* Formatted and colorized terminal output
* Built-in XML support
* Python 2.7 and 3.x support
* Linux, macOS and Windows support

Installation
============

A universal installation method (that works on Windows, Mac OS X, Linux, …,
and always provides the latest version) is to use `pip`_:

.. code-block:: bash

    # Make sure we have an up-to-date version of pip and setuptools:
    $ pip install --upgrade pip setuptools

    $ pip install --upgrade httpaws


(If ``pip`` installation fails for some reason, you can try ``easy_install httpaws`` as a fallback.)

Python version
--------------

Although Python 2.7 is supported as well, it is strongly recommended to
install httpAWS against the latest Python 3.x whenever possible. That will
ensure that some of the newer HTTP features, such as
`SNI (Server Name Indication)`_, work out of the box.
Python 3 is the default for Homebrew installations starting with version 0.9.4.

Unstable version
----------------

You can also install the latest unreleased development version directly from
the ``master`` branch on GitHub.  It is a work-in-progress of a future stable
release so the experience might be not as smooth.

.. code-block:: bash

    $ pip install -U https://github.com/http-aws/http-aws/archive/master.tar.gz

Usage
=====

Hello World:


.. code-block:: bash

    $ httpaws -s ec2 DescribeVpcs

Synopsis:

.. code-block:: bash

    $ httpaws [flags] <API>

See also ``httpaws -h`` for detailed help:

.. code-block:: bash

    $ httpaws -h
    usage: httpaws [-h] [-r REGION] [-s SERVICE] [-e ENDPOINT] [-c CREDS]
                   [-v VERSION] [-p] [-w]
                   api

    httpaws v0.0.2: A CLI HTTP client for AWS services with syntax highlighting

    positional arguments:
      api                   name of the API to call - e.g. "DescribeVpcs"

    optional arguments:
      -h, --help            show this help message and exit
      -r REGION, --region REGION
                            AWS region. Overrides config/env - e.g. us-east-1
      -s SERVICE, --service SERVICE
                            AWS service - e.g. ec2, s3, etc.
      -e ENDPOINT, --endpoint ENDPOINT
                            override command's default URL with the given URL -
                            e.g. ec2.us-east-1.amazonaws.com
      -c CREDS, --creds CREDS
                            override AWS Access Key Id and AWS Secret Access Key -
                            i.e. <Access_Key>:<Secret_Key>
      -v VERSION, --version VERSION
                            API version to use for the service
      -p, --paginate        paginate long output
      -w, --wrap            wrap long lines in paginated output (instead of chop)

    See the AWS Documentation for API references for each service:
    https://docs.aws.amazon.com

Authentication
==============

The currently supported authentication scheme is provided by the
`aws-requests-auth <https://github.com/DavidMuller/aws-requests-auth>`_ Python module. The two modes are are Automatic
and Manual. There is one flag that controls authentication:

===================     ===========================================================================
``--creds, -c``         Pass a ``<AWS_Access_Key_Id>:<AWS_Secret_Access_Key>`` pair as the argument
===================     ===========================================================================

Automatic auth
--------------

If the ``-c`` flag is not provided, then httpAWS will attempt to automatically gather your AWS credentials using
``botocore``.

.. code-block:: bash

    $ httpaws DescribeVpcs

Manual auth
-----------

.. code-block:: bash

    $ http -c <Access_Key>:<Secret_Key> DescribeVpcs

HTTP redirects
==============

HTTP redirects are not followed and only the first esponse is shown.

Output options
==============

At this time, httpAWS only outputs the final response and the whole response
message is printed (headers as well as the body).

Terminal output
===============

httpAWS does several things by default in order to make its terminal output
easy to read.


Colors and formatting
---------------------

Syntax highlighting is applied to HTTP headers bodies (where it makes
sense).

Also, the following formatting is applied:

* XML data is indented and unicode escapes are converted to the characters they represent.

Redirected output
=================

By default, httpAWS sends all output to ``stdout``.

The reason is to make piping httpAWS's output to other programs work with no extra flags. Most of the time, only the raw
response body is of an interest when the output is redirected.

Force colorizing and formatting, and show both the request and the response in
``less`` pager:

.. code-block:: bash

    $ httpaws -p DescribeVpcs


The ``-p`` flag tells httpAWS to pipe the output to ``less`` and to interpret color escape sequences included
httpAWS`s output.


Piping output
-------------

You can also redirect the response body to another program:

.. code-block:: bash

    $ httpaws -s s3 List |  grep "MagnumOpus.txt"

Responses
=========

Responses are downloaded synchronously and printed when the download is complete which is convenient for formatting and
coloring moderate sized responses.  However, if you want to download large files without using too much memory, this isn't
the tool you are looking for.

Sessions
========

At this time every request httpAWS makes is completely independent of any previous ones to the same host.


In the future, httpAWS may also supports persistent sessions.

Config
======

httpAWS uses the same config files as used by the ``aws cli``.


Config file location
--------------------

The default location of the configuration files are ``~/.aws/config`` and ``~/.aws/credentials``.

Configurable options
--------------------

The default AWS region is read from the ``config`` file, while the default AWS access and secret keys are read from the
``credentials`` file.

Best practices
--------------

The ``-p`` option for paginating long output is excellent when a human is reading this output, but
is not typically desirable during non-interactive invocations. You most likely do not want to use
use the ``-p`` option when httpAWS is invoke from example form a cron job.  Also, if you wnat to redirect or
pipe the output of httpAWS, the ``-p`` flag should also be avoided.

Meta
====

User support
------------

Please use the following support channels:

* `GitHub issues <https://github.com/http-aws/http-aws/issues>`_
  for bug reports, feature requests, and to ask questions
* `GitHub pull requests <https://github.com/http-aws/http-aws/pulls>`_
  for bug fixes and feature submissions

Related projects
----------------

Dependencies
~~~~~~~~~~~~

Under the hood, httpAWS uses these amazing libraries:

* `Requests <http://python-requests.org>`_
  — Python HTTP library for humans
* `aws-requests-auth <https://github.com/DavidMuller/aws-requests-auth>`_
  — AWS signature version 4 signing process for the Python requests module
* `botocore <https://github.com/boto/botocore>`_
  - The low-level, core functionality of boto 3 (the official AWS Python SDK)
* `Pygments <http://pygments.org>`_
  — Python syntax highlighter
* `Colorama <https://github.com/tartley/colorama>`_
  — Simple cross-platform colored terminal text in Python
* `lxml <https://lxml.de>`_
  — XML with Python

Alternatives
~~~~~~~~~~~~

* `HTTPie <https://httpie.org>`_ — an awesome and much more feature rich HTTP CLI that isn't specific to AWS
* `curl <https://curl.haxx.se>`_ — a "Swiss army knife" command line tool and library for transferring data with URLs

Warning
~~~~~~~

This tool is intended for development and educational purposes.  It is NOT intended for robust and reliable
administration of AWS services.  For interaction with production AWS services, it is highly recommended that you use
an officially supported tool specifically designed for that purpose such as any of the following:

* `AWS Console <https://aws.amazon.com/console>`_
* `AWS CLI <https://aws.amazon.com/cli>`_
* `AWS Shell <https://github.com/awslabs/aws-shell>`_
* `AWS SDK for Python (boto3) <https://aws.amazon.com/sdk-for-python>`_

Contributing
------------

See `CONTRIBUTING.md <https://github.com/http-aws/http-aws/blob/master/CONTRIBUTING.md>`_.

Change log
----------

See `CHANGELOG.md <https://github.com/http-aws/http-aws/blob/master/CHANGELOG.md>`_.

Licence
-------

Apache 2.0: `LICENSE <https://github.com/http-aws/http-aws/blob/master/LICENSE>`_.

Authors
-------

`Todd Leonhardt`_ created httpaws and `these fine people`_ have contributed.

.. _pip: https://pip.pypa.io/en/stable/installing/
.. _Github API: http://developer.github.com/v3/issues/comments/#create-a-comment
.. _these fine people: https://github.com/http-aws/http-aws/graphs/contributors
.. _Todd Leonhardt: https://github.com/tleonhardt
