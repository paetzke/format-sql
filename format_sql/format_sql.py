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
        text = f.read()
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass
    return text


def format_text(text):
    queries = re.findall(r'([ ]*)[_\w\d.]*\s*=*\s*\(*"{3}(\s*.*?;*\s*)"{3}',
                         text, re.DOTALL)

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

        text = text.replace(old_query, '\n%s ' % '\n'.join(fs))

    return text


def format_file(filename):
    content = load_from_file(filename)
    content = format_text(content)

    if content:
        content = content.encode('utf-8')
        with open(filename, 'wb') as f:
            f.write(content)


def format_files_in_directory(dirname):
    for root, unused_dir, files in os.walk(dirname):
        for item in fnmatch.filter(files, "*.py"):
            fname = os.path.join(root, item)
            yield fname


def format_path(pathname):
    pathname = os.path.abspath(pathname)
    if os.path.isfile(pathname):
        yield pathname
    elif os.path.isdir(pathname):
        for filename in format_files_in_directory(pathname):
            yield filename


def main():
    for arg in sys.argv[1:]:
        for filename in format_path(arg):
            print(filename)
            format_file(filename)


if __name__ == '__main__':
    main()
