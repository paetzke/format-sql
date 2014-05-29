# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from .parser import parse
from .styler import style
from .tokenizer import normalize_sql, tokenize


def format_sql(sql):
    sql, has_semicolon = normalize_sql(sql)
    tokens = list(tokenize(sql))
    parsed = parse(tokens)
    styled = style(parsed)
    if has_semicolon:
        styled += ';'
    return styled
