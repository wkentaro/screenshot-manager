#!/usr/bin/env python

from __future__ import print_function

from setuptools import find_packages
from setuptools import setup
import shlex
import subprocess
import sys


version = "1.0.4"


# release helper
if sys.argv[-1] == "release":
    commands = [
        "git pull origin master",
        "git tag v{0}".format(version),
        "git push origin master --tags",
        "python setup.py sdist",
        "twine upload dist/screenshot-manager-{0}.tar.gz".format(version),
    ]
    for cmd in commands:
        print("+ {0}".format(cmd))
        subprocess.check_call(shlex.split(cmd))
    sys.exit(0)


def get_long_description():
    with open("README.md") as f:
        long_description = f.read()

    try:
        import github2pypi

        return github2pypi.replace_url(
            slug="wkentaro/screenshot-manager", content=long_description
        )
    except Exception:
        return long_description


setup(
    name="screenshot-manager",
    version=version,
    packages=find_packages(),
    install_requires=[],
    description="Copy screenshots and organize.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Kentaro Wada",
    author_email="www.kentaro.wada@gmail.com",
    url="http://github.com/wkentaro/screenshot-manager",
    license="MIT",
    keywords="utility",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={
        "console_scripts": ["screenshot-manager=screenshot_manager.cli:main"]
    },
)
