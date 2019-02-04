#!/usr/bin/python3

from setuptools import setup
import os

def strip_comments(l):
    return l.split('#', 1)[0].strip()

def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(os.path.join(os.getcwd(), *f)).readlines()]))

setup(
    name='lagopus-birdwatcher',
    install_requires=reqs('requirements.txt'),
    test_suite='nose.collector'
)
