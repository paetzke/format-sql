#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (f.paetzke@gmail.com)
All rights reserved.

"""
from __future__ import print_function

import fnmatch
import os
import re
import sys

import sqlparse

from .formatter import format_sql


def load_from_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    try:
        content = unicode(content, 'utf-8')
    except NameError:
        pass
    return content.splitlines()


def _read_dir(dirname):
    for root, unused_dir, files in os.walk(dirname):
        for item in fnmatch.filter(files, "*.py"):
            fname = os.path.join(root, item)
            yield fname


def _handle_file(filename):
    content = load_from_file(filename)
    content = format_sql(content)

    if content:
        content = '\n'.join(content)
        content = content.encode('utf-8')
        with open(filename, 'wb') as f:
            f.write(content)
            f.write('\n')


def format_sql(lines):
    content = '\n'.join(lines)

    queries = re.findall(r'([ ]*)[_\w\d]*\s*=*\s*"{3}(\s*.*?;*\s*)"{3}',
                         content, re.DOTALL)

    for indent, query in queries:
        indent += ' ' * 4
        old_query = query
        query = ' '.join(query.split())

        first = query.split()
        if not first:
            continue

        first = first[0].lower()
        if not first in ['select']:
            continue

        fs = []
        fmt = format_sql(query).splitlines()
        for line in fmt:
            fs.append(indent + line.rstrip())

        content = content.replace(old_query, '\n%s ' % '\n'.join(fs))

    return content.split('\n')


def main():
    for arg in sys.argv[1:]:
        pathname = os.path.abspath(arg)
        if os.path.isfile(pathname):
            print(pathname)
            _handle_file(pathname)
        elif os.path.isdir(pathname):
            for filename in _read_dir(pathname):
                print(filename)
                _handle_file(filename)
        else:
            print('Unknown path %s' % pathname)


if __name__ == '__main__':
    main()
