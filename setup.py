# This is purely the result of trial and error.

import codecs
from setuptools import setup, find_packages

import httpaws

install_requires = [
    'requests>=2.19.0',
    'aws-requests-auth>=0.4.0',
    'botocore>=1.12.0',
    'colorama>=0.3.0',
    'pygments>=2.3.0',
    'lxml>=4.0.0',
]


def long_description():
    with codecs.open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name='httpaws',
    version=httpaws.__version__,
    description=httpaws.__doc__.strip(),
    long_description=long_description(),
    url='https://github.com/http-aws/http-aws',
    download_url='https://github.com/http-aws/http-aws',
    author=httpaws.__author__,
    author_email='todd.leonhardt@gmail.com',
    license=httpaws.__licence__,
    platforms=['any'],
    packages=find_packages(),
    keywords='http cli aws',
    python_requires='>=2.7',
    entry_points={
        'console_scripts': [
            'httpaws = httpaws.__main__:main',
        ],
    },
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ],
)
