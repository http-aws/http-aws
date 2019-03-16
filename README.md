# httpaws
httpAWS - a CLI, [cURL](https://curl.haxx.se)-like tool for [AWS](https://aws.amazon.com) services.

Directly make HTTP calls to AWS service endpoints using the requsts and aws-requests-auth modules.

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
- [WS SDK for Python (boto3)](https://aws.amazon.com/sdk-for-python/)
