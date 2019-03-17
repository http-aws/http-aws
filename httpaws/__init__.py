"""
httpAWS - a CLI, cURL-like tool for AWS services.

"""
__version__ = '0.0.3'
__author__ = 'Todd Leonhardt'
__licence__ = 'Apache 2.0'


class ExitStatus:
    """Program exit code constants."""
    SUCCESS = 0
    ERROR = 1

    # 128+2 SIGINT <http://www.tldp.org/LDP/abs/html/exitcodes.html>
    ERROR_CTRL_C = 130
