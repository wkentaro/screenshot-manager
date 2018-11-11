#!/usr/bin/env python

from __future__ import print_function

from setuptools import find_packages
from setuptools import setup
import shlex
import subprocess
# import sys


def git_hash():
    cmd = 'git log -1 --format="%h"'
    try:
        hash_ = subprocess.check_output(shlex.split(cmd)).decode().strip()
    except subprocess.CalledProcessError:
        hash_ = None
    return hash_


version = '0.2.0-0'

hash_ = git_hash()
if hash_ is not None:
    version = '%s.%s' % (version, hash_)


# # release helper
# if sys.argv[-1] == 'release':
#     commands = [
#         'python setup.py sdist upload',
#         'git tag v{0}'.format(version),
#         'git push origin master --tag',
#     ]
#     for cmd in commands:
#         subprocess.check_call(shlex.split(cmd))
#     sys.exit(0)


setup(
    name='screenshot_manager',
    version=version,
    packages=find_packages(),
    install_requires=[],
    description='Copy screenshots and organize.',
    long_description=open('README.md').read(),
    author='Kentaro Wada',
    author_email='www.kentaro.wada@gmail.com',
    url='http://github.com/wkentaro/screenshot-manager',
    license='MIT',
    keywords='utility',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Topic :: Internet :: WWW/HTTP',
    ],
    entry_points={
        'console_scripts': ['screenshot-manager=screenshot_manager.cli:main']
    },
)
