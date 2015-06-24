#!/usr/bin/env python
# borrowed from pgcli

from __future__ import print_function
import re
import ast
import subprocess
import sys

DEBUG = True


def version(version_file):
    _version_re = re.compile(r'__version__\s+=\s+(.*)')

    with open(version_file, 'rb') as f:
        ver = str(ast.literal_eval(_version_re.search(
            f.read().decode('utf-8')).group(1)))

    return ver


def commit_for_release(version_file, ver):
    cmd = ['git', 'reset']
    print(' '.join(cmd))
    subprocess.check_output(cmd)
    cmd = ['git', 'add', version_file]
    print(' '.join(cmd))
    subprocess.check_output(cmd)
    cmd = ['git', 'commit', '--message', 'Releasing version %s' % ver]
    print(' '.join(cmd))
    subprocess.check_output(cmd)


def create_git_tag(tag_name):
    cmd = ['git', 'tag', tag_name]
    print(' '.join(cmd))
    subprocess.check_output(cmd)


def register_with_pypi():
    cmd = ['python', 'setup.py', 'register']
    print(' '.join(cmd))
    subprocess.check_output(cmd)


def create_source_tarball():
    cmd = ['python', 'setup.py', 'sdist']
    print(' '.join(cmd))
    subprocess.check_output(cmd)


def push_to_github():
    cmd = ['git', 'push', '-u', 'origin']
    print(' '.join(cmd))
    subprocess.check_output(cmd)


def push_tags_to_github():
    cmd = ['git', 'push', '-u',  '--tags', 'origin']
    print(' '.join(cmd))
    subprocess.check_output(cmd)


if __name__ == '__main__':
    if DEBUG:
        subprocess.check_output = lambda x: x

    ver = version('flask_transfer/__init__.py')
    tests = raw_input("Did you remember to run the tests? (y/N) ")
    if tests.lower() != 'y':
        sys.exit(1)

    print('Releasing Version:', ver)
    choice = raw_input('Are you sure? (y/N) ')
    if choice.lower() != 'y':
        sys.exit(1)

    commit_for_release('flask_transfer/__init__.py', ver)
    create_git_tag('v%s' % ver)
    register_with_pypi()
    create_source_tarball()
    push_to_github()
    push_tags_to_github()
