"""
httpAWS - a CLI, cURL-like tool for AWS services.

Directly make HTTP calls to AWS service endpoints using the requsts and aws-requests-auth modules.

This is a low-level command-line tool intended for use by developers so that they can easily make direct HTTP calls
to AWS services.  It is effectively a command-line programmatic replacement for using a graphical tool like Postman
(https://www.getpostman.com) and was inspired by tools like HTTPie (https://httpie.org) but is specific to AWS services.

WARNING: This tool is intended for development and educational purposes.  It is NOT intended for robust and reliable
administration of AWS services.  For interaction with production AWS services, it is highly recommended that you use an
officially supported tool specifically designed for that purpose such as any of the following:
- AWS Console
    * https://aws.amazon.com
- AWS CLI
    * https://aws.amazon.com/cli/
- AWS Shell
    * https://github.com/awslabs/aws-shell
- AWS SDK for Python (boto3)
    * https://aws.amazon.com/sdk-for-python/
"""
__version__ = '0.0.1'
__author__ = 'Todd Leonhardt'
__licence__ = 'Apache 2.0'


class ExitStatus:
    """Program exit code constants."""
    SUCCESS = 0
    ERROR = 1

    # 128+2 SIGINT <http://www.tldp.org/LDP/abs/html/exitcodes.html>
    ERROR_CTRL_C = 130
