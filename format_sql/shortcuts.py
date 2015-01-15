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


def format_sql(s):
    tokens = list(tokenize(s))
    parsed = list(parse(tokens))
    styled = style(parsed)
    return styled
