# coding=utf-8
"""This module provides the main functionality of httpAWS.
Invocation flow:
  1. Read, validate and process the input (args, `stdin`).
  2. Create and send a request.
  3. Stream, and possibly process and format, the parts
     of the request-response exchange selected by output options.
  4. Simultaneously write to `stdout`
  5. Exit.
"""
import argparse
import os
import sys

import colorama
from colorama import Fore
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import TerminalFormatter
import requests

from httpaws import ExitStatus


def perror(msg, color=Fore.LIGHTRED_EX):
    """ Print error message to sys.stderr.

    :param msg: an error message to print out
    :param color: (optional) color escape to output error with
    """
    err_msg = "{}\n".format(msg)
    err_msg = color + err_msg + Fore.RESET
    sys.stderr.write(err_msg)


# Set the pager(s) for use with the ppaged() method for displaying output using a pager
if sys.platform.startswith('win'):
    pager_wrap = pager_chop = 'more'
else:
    # Here is the meaning of the various flags we are using with the less command:
    # -S causes lines longer than the screen width to be chopped (truncated) rather than wrapped
    # -R causes ANSI "color" escape sequences to be output in raw form (i.e. colors are displayed)
    # -X disables sending the termcap initialization and deinitialization strings to the terminal
    # -F causes less to automatically exit if the entire file can be displayed on the first screen
    pager_wrap = 'less -RXF'
    pager_chop = 'less -SRXF'


def ppaged(msg, end='\n', wrap=False):
    """Print output using a pager if it would go off screen and stdout isn't currently being redirected.

    Never uses a pager inside of a script (Python or text) or when output is being redirected or piped or when
    stdout or stdin are not a fully functional terminal.

    :param msg: message to print to current stdout - anything convertible to a str with '{}'.format() is OK
    :param end: string appended after the end of the message if not already present, default a newline
    :param wrap: False -> causes lines longer than the screen width to be chopped (truncated) rather than wrapped
                          - truncated text is still accessible by scrolling with the right & left arrow keys
                          - chopping is ideal for displaying wide tabular data as is done in utilities like pgcli
                 True -> causes lines longer than the screen width to wrap to the next line
                          - wrapping is ideal when you want to keep users from having to use horizontal scrolling

    WARNING: On Windows, the text always wraps regardless of what the chop argument is set to
    """
    import subprocess
    if msg is not None and msg != '':
        msg_str = '{}'.format(msg)
        if not msg_str.endswith(end):
            msg_str += end

        # Attempt to detect if we are not running within a fully functional terminal.
        # Don't try to use the pager when being run by a continuous integration system like Jenkins + pexpect.
        functional_terminal = False

        if sys.stdin.isatty() and sys.stdout.isatty():
            if sys.platform.startswith('win') or os.environ.get('TERM') is not None:
                functional_terminal = True

        # Only attempt to use a pager if actually running in a real fully functional terminal
        if functional_terminal:
            pager = pager_chop
            if wrap:
                pager = pager_wrap
            pipe_proc = subprocess.Popen(pager, shell=True, stdin=subprocess.PIPE)
            try:
                pipe_proc.stdin.write(msg_str.encode('utf-8', 'replace'))
                pipe_proc.stdin.close()
            except (OSError, KeyboardInterrupt):
                pass

            # Less doesn't respect ^C, but catches it for its own UI purposes (aborting search etc. inside less)
            while True:
                try:
                    pipe_proc.wait()
                except KeyboardInterrupt:
                    pass
                else:
                    break
        else:
            print(msg_str)


def main(argv=None):
    """Run when invoked from the command-line."""
    colorama.init(autoreset=True)
    # Create an arparse argument parser for parsing command-line arguments
    desc = 'A command line HTTP client for AWS services with an intuitive UI, XML support and syntax highlighting.'
    epilog = 'See the AWS Documentation for API references for each service:  https://docs.aws.amazon.com'
    parser = argparse.ArgumentParser(description=desc, epilog=epilog, prog='http_aws')
    parser.add_argument('-r', '--region', help='The region to use. Overrides config/env settings.')
    parser.add_argument('-s', '--service', help='AWS service - e.g. ec2, s3, etc.', default='ec2')
    parser.add_argument('-e', '--endpoint',
                        help="Override command's default URL with the given URL - e.g. ec2.us-east-1.amazonaws.com")
    parser.add_argument('-c', '--creds',
                        help="Override AWS Access Key Id and AWS Secret Access Key - i.e. <Access_Key>:<Secret_Key>")
    parser.add_argument('-v', '--version', help='API version to use for the service', default='2015-10-01')
    parser.add_argument('-p', '--paginate', action='store_true', help='Paginate long output')
    parser.add_argument('-w', '--wrap', action='store_true',
                        help='Wrap long lines in paginated output instead of chopping them off')
    parser.add_argument('api', help='Name of the API to call - e.g. "DescribeVpcs" (for ec2 service)')
    args = parser.parse_args(argv)

    # --- Configure AWS basics ---

    # Configure AWS region
    aws_region = 'us-east-1'    # Default if not overriden on command-line or specified in config file
    if args.region:
        aws_region = args.region
    else:
        import os
        # Read the region from the ~/.aws/config file if it exists
        try:
            with open(os.path.expanduser('~/.aws/config')) as f:
                data = f.read()
                lines = data.splitlines()
                for line in lines:
                    if line.startswith('region = '):
                        aws_region = line.split('region = ')[1]
                        break
        except (FileNotFoundError, PermissionError):
            pass

    # Configure AWS service
    if args.service:
        aws_service = args.service
    else:
        aws_service = 'ec2'  # Default if not overriden on command-line

    # Configure AWS endpoint
    if args.endpoint:
        aws_endpoint = args.endpoint
    else:
        aws_endpoint = '{}.{}.amazonaws.com'.format(aws_service, aws_region)

    if args.creds:
        from aws_requests_auth.aws_auth import AWSRequestsAuth
        # Use the specified AWS access and secret key
        try:
            access_key, secret_key = args.creds.split(':')
            auth = AWSRequestsAuth(aws_access_key=access_key,
                                   aws_secret_access_key=secret_key,
                                   aws_host=aws_endpoint,
                                   aws_region=aws_region,
                                   aws_service=aws_service)
        except ValueError:
            perror('Credentials must be proviced in the format "<AWS_Access_Key_Id>:<AWS_Secret_Access_key>')
            return ExitStatus.ERROR
    else:
        # This line will fail if you do not have both aws-requests-auth and botocore installed
        from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
        # Use Boto to automatically gather AWS credentials from environment variables, AWS config files, or IAM Role
        auth = BotoAWSRequestsAuth(aws_host=aws_endpoint,
                                   aws_region=aws_region,
                                   aws_service=aws_service)

    # Configure details of the API call
    api = args.api
    api_version = args.version
    params = {'Action': api, 'Version': api_version}
    url = 'https://{}'.format(aws_endpoint)

    # Send a GET request
    try:
        # TODO: Support PUT requests for Mutating API calls
        response = requests.get(url=url, params=params, auth=auth)
    except requests.exceptions.ConnectionError:
        perror('Error connecting to host {!r}'.format(url))
        return ExitStatus.ERROR

    # Gather response details
    response_text = 'Response code: {}'.format(response.status_code)
    header_text = 'Headers: {}'.format(response.headers)

    # Convert the response content from an encoded byte string to a Unicode string
    response_bytes = response.content
    response_str = response_bytes.decode()

    # If the respose is XML, ensure that it is nicely formatted with good indenting and newlines
    if response_str.startswith('<?xml'):
        try:
            import lxml.etree as etree
            response_bytes = etree.tostring(etree.fromstring(response.content), pretty_print=True)
        except ImportError:
            pass

    # Pretty-print the content of the response with syntax highlighting for readability
    highlighted_text = highlight(response_bytes, guess_lexer(response_str), TerminalFormatter())
    output_text = '{}\n{}\n{}'.format(response_text, header_text, highlighted_text)
    if args.paginate:
        ppaged(output_text, wrap=args.wrap)
    else:
        print(output_text)
    return ExitStatus.SUCCESS
