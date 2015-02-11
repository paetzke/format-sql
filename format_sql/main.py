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
from format_sql.util import print_data, print_non_data


def _get_args(call_args):
    parser = ArgumentParser('format-sql')

    parser.add_argument('--types', dest='types', type=str,
                        action='append',
                        help='Only process these given file types.')
    parser.add_argument('paths', type=str, nargs='+')
    parser.add_argument('-r', '--recursive', dest='recursive',
                        action='store_true', default=False,
                        help='Process files found in subdirectories.')
    parser.add_argument('--no-semicolon', action='store_true', default=False,
                        help='Try to detect SQL queries with no trailing semicolon.')
    parser.add_argument('--version', action='version',
                        version='format-sql 0.6.0')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False,
                        help='Print available debug information.')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true', default=False,
                        help='Print the altered output and do not change the file.')

    args, _unused_unknown_args = parser.parse_known_args(call_args)
    if not args.types:
        args.types = []

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
    filenames = _get_filenames(args.paths, args.recursive)

    if args.types:
        filenames = filter(lambda fn: fn.endswith(tuple(args.types)), filenames)

    for filename in filenames:
        print_non_data(filename)

        if filename.lower().endswith('.py'):
            lines = handle_py_file(filename, args.debug)
        else:
            lines = handle_sql_file(filename, args.debug)

        _write_back(filename, lines, args.dry_run)


def get_statements(lines):
    regex = r'(\s*)[_\w\d\.]*\s*=*\s*[_\w\d\.]*\s*\(*("""|\'\'\')(\s*.*?;*\s*)\2'
    queries = re.findall(regex, lines, re.DOTALL)
    for indent, query_quote_start, query in queries:
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

        yield old_query, query, indent


def handle_py_file(filename, debug=False):
    with open(filename) as f:
        lines = f.read()

    for old_query, query, indent in get_statements(lines):
        if debug:
            print_non_data('Found query: %s' % query)

        try:
            fmt = format_sql(query, debug)
        except InvalidSQL as e:
            print_non_data(e)
            continue

        fs = []
        for line in fmt:
            s = '%s%s' % (indent, line)
            fs.append(s.rstrip())

        lines = lines.replace(old_query, '\n%s ' % '\n'.join(fs))
    return lines


def handle_sql_file(filename, debug=False):
    with open(filename) as f:
        lines = f.read()

    try:
        sql = format_sql(lines, debug)
    except InvalidSQL as e:
        print_non_data(e)
        return

    lines = '\n'.join(sql)
    return lines


def _write_back(filename, lines, dry_run=False):
    if dry_run:
        print_data(lines)
    else:
        with open(filename, 'w') as f:
            f.write(lines)


if __name__ == '__main__':
    main()
