#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from __future__ import print_function

import sys
from argparse import ArgumentParser
from itertools import product

from .file_handling import _get_file_in_path, format_file


def _get_args(call_args):
    parser = ArgumentParser('format-sql')

    parser.add_argument('--types', dest='types', type=str, nargs='*',
                        default=['py'],
                        help='Process given file types. Default value is "py".')
    parser.add_argument('paths', type=str, nargs='+')
    parser.add_argument('-r', '--recursive', dest='recursive',
                        action='store_true', default=False,
                        help='Process files found in subdirectories.')
    parser.add_argument('--no-semicolon', action='store_true', default=False,
                        help='Try to detect SQL queries with no trailing semicolon.')

    args, _unused_unknown_args = parser.parse_known_args(call_args)
    return args


def main(call_args=sys.argv):
    args = _get_args(call_args)

    for file_type, path in product(args.types, args.paths):
        for filename in _get_file_in_path(path, file_type, args.recursive):
            print(filename)
            format_file(filename, file_type, not args.no_semicolon)


if __name__ == '__main__':
    main()
