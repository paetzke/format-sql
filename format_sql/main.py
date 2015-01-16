#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014-2015, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from __future__ import print_function

import os
import re
import sys
from argparse import ArgumentParser
from glob import glob

from format_sql.parser import InvalidSQL
from format_sql.shortcuts import format_sql


def _get_args(call_args):
    parser = ArgumentParser('format-sql')

    parser.add_argument('--types', dest='types', type=str,
                        choices=['py', 'sql'],
                        action='append',
                        help='Process given file types. Default value is "py".')
    parser.add_argument('paths', type=str, nargs='+')
    parser.add_argument('-r', '--recursive', dest='recursive',
                        action='store_true', default=False,
                        help='Process files found in subdirectories.')
    parser.add_argument('--no-semicolon', action='store_true', default=False,
                        help='Try to detect SQL queries with no trailing semicolon.')

    args, _unused_unknown_args = parser.parse_known_args(call_args)
    if not args.types:
        args.types = ['py']

    return args


def _get_filenames(paths, recursive):
    filenames = set()
    for path in paths:
        path = os.path.abspath(path)
        if os.path.isfile(path):
            filenames.add(path)
        elif os.path.isdir(path):
            if recursive:
                for dirpath, dirnames, fnames in os.walk(path):
                    filenames.update(os.path.join(dirpath, fn)
                                     for fn in fnames)
            else:
                if not path.endswith('/'):
                    path += '/'
                filenames.update(glob('%s*' % path))
    return filenames


def main(args=sys.argv[1:]):
    args = _get_args(args)
    all_filenames = _get_filenames(args.paths, args.recursive)
    filenames = filter(lambda fn: fn.endswith(tuple(args.types)), all_filenames)

    for filename in filenames:
        print(filename)
        if filename.lower().endswith('.py'):
            handle_py_file(filename)
        elif filename.lower().endswith('.sql'):
            handle_sql_file(filename)


def handle_py_file(filename):
    with open(filename) as f:
        lines = f.read()

    regex = r'(\s*)[_\w\d\.]*\s*=*\s*[_\w\d\.]*\s*\(*"{3}(\s*.*?;*\s*)"{3}'
    queries = re.findall(regex, lines, re.DOTALL)
    for indent, query in queries:
        indent = indent.strip('\n')
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

        try:
            fmt = format_sql(query)
        except InvalidSQL as e:
            print(e, file=sys.stderr)
            continue

        for line in fmt:
            s = '%s%s' % (indent, line)
            fs.append(s.rstrip())

        lines = lines.replace(old_query, '\n%s ' % '\n'.join(fs))

    _write_back(filename, lines)


def handle_sql_file(filename):
    with open(filename) as f:
        lines = f.read()

    try:
        sql = format_sql(lines)
    except InvalidSQL as e:
        print(e, file=sys.stderr)
        return

    lines = '\n'.join(sql)
    _write_back(filename, lines)


def _write_back(filename, lines):
    with open(filename, 'w') as f:
        f.write(lines)


if __name__ == '__main__':
    main()
