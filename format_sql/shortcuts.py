# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014-2015, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from format_sql.parser import parse
from format_sql.styler import style
from format_sql.tokenizer import tokenize
from format_sql.util import print_non_data


def format_sql(s, debug=False):
    tokens = list(tokenize(s))
    if debug:
        print_non_data('Tokens: %s' % tokens)
    parsed = list(parse(tokens))
    if debug:
        print_non_data('Statements: %s' % parsed)
    styled = style(parsed)
    if debug:
        print_non_data('Output: %s' % styled)
    return styled
