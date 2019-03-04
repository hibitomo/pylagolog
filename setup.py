#!/usr/bin/python3

from setuptools import setup
import os

def strip_comments(l):
    return l.split('#', 1)[0].strip()

def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(os.path.join(os.getcwd(), *f)).readlines()]))

setup(
    name='birdwatcher',
    version='0.0.1',
    install_requires=reqs('requirements.txt'),
    test_suite='nose.collector',
    entry_points={
        "console_scripts":[
            "birdwatcher = birdwatcher.cmd.birdwatcher_base:main"
        ]
    }
)
