#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from __future__ import print_function

import fnmatch
import os
import re

from .formatter import format_sql


def load_from_file(filename):
    with open(filename, 'r') as f:
        text = f.read()
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass
    return text


def _get_file_in_path(path, file_type, recursive):
    pathname = os.path.abspath(path)
    if os.path.isfile(pathname):
        yield pathname
    elif os.path.isdir(pathname) and recursive:
        for root, unused_dir, files in os.walk(pathname):
            for item in fnmatch.filter(files, '*.' + file_type):
                fname = os.path.join(root, item)
                yield fname


def format_file(filename, file_type):
    try:
        format_text = {
            'py': _format_py_text,
            'sql': _format_sql_text,
        }[file_type]
    except KeyError:
        return

    content = load_from_file(filename)
    content = format_text(content)

    if content:
        content = content.encode('utf-8')
        with open(filename, 'wb') as f:
            f.write(content)


def _format_py_text(text):
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


def _format_sql_text(text):
    if not text.lower().startswith('select '):
        return

    return format_sql(text) + '\n'
