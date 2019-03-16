# httpAWS: a CLI, [cURL](https://curl.haxx.se)-like tool for [AWS](https://aws.amazon.com) services

httpAWS is a command line HTTP client for AWS services. Its goal is to make CLI interaction with AWS web services as 
human-friendly as possible. It provides a simple ``httpaws`` command that allows for sending HTTP requests to AWS 
services using a simple and natural syntax, and displays colorized output. httpAWS can be used for testing, debugging, 
and generally interacting direly with AWS services with HTTP requests.

httpAWS directly makes HTTP calls to AWS service endpoints using the [requests](http://docs.python-requests.org) and 
[aws-requests-auth](https://github.com/DavidMuller/aws-requests-auth) modules.

This is a low-level command-line tool intended for use by developers so that they can easily make direct HTTP calls
to AWS services.  It is effectively a command-line programmatic replacement for using a graphical tool like 
[Postman](https://www.getpostman.com) and was inspired by tools like [HTTPie](https://httpie.org) but is specific to 
AWS services.

**WARNING**: *This tool is intended for development and educational purposes*.  It is NOT intended for robust and reliable
administration of AWS services.  For interaction with production AWS services, it is highly recommended that you use an
officially supported tool specifically designed for that purpose such as any of the following:
- [AWS Console](https://aws.amazon.com/console)
- [AWS CLI](https://aws.amazon.com/cli/)
- [AWS Shell](https://github.com/awslabs/aws-shell)
- [AWS SDK for Python (boto3)](https://aws.amazon.com/sdk-for-python/)

# Main Features
- Expressive and intuitive syntax
- Formatted and colorized terminal output
- Built-in XML support
- Python 2.7 and 3.x support
- Linux, macOS and Windows support

# Installation
A universal installation method (that works on Windows, Mac OS X, Linux, …, and always provides the latest version) is 
to use [pip](https://pypi.org/project/pip/):

```sh
# Make sure we have an up-to-date version of pip and setuptools:
$ pip install -U pip setuptools

$ pip install -U httpaws
```

# Usage
Hello World:

```sh
$ httpaws -s ec2 DescribeVpcs
```
The above command calls the **DescribeVpcs** API on the EC2 service using the credentials and default region found in
your *~/.aws* directory.

Synopsis:
```sh
$ httpaws [flags] <API>
```

See also ``httpaws -h`` for detailed help:
```sh
httpaws -h
usage: http_aws [-h] [-r REGION] [-s SERVICE] [-e ENDPOINT] [-c CREDS]
                [-v VERSION] [-p] [-w]
                api

A command line HTTP client for AWS services with an intuitive UI, XML support
and syntax highlighting.

positional arguments:
  api                   Name of the API to call - e.g. "DescribeVpcs" (for ec2
                        service)

optional arguments:
  -h, --help            show this help message and exit
  -r REGION, --region REGION
                        The region to use. Overrides config/env settings.
  -s SERVICE, --service SERVICE
                        AWS service - e.g. ec2, s3, etc.
  -e ENDPOINT, --endpoint ENDPOINT
                        Override command's default URL with the given URL -
                        e.g. ec2.us-east-1.amazonaws.com
  -c CREDS, --creds CREDS
                        Override AWS Access Key Id and AWS Secret Access Key -
                        i.e. <Access_Key>:<Secret_Key>
  -v VERSION, --version VERSION
                        API version to use for the service
  -p, --paginate        Paginate long output
  -w, --wrap            Wrap long lines in paginated output instead of
                        chopping them off

See the AWS Documentation for API references for each service:
https://docs.aws.amazon.com
```

