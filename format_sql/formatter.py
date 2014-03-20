# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (f.paetzke@gmail.com)
All rights reserved.

"""
import sqlparse
from sqlparse.sql import (Comparison, Identifier, IdentifierList, Parenthesis,
                          Where)


def _filter(tokens):
    return (token for token in tokens if not token.is_whitespace())


def _val(token, indent=0):
    if isinstance(token, Parenthesis):
        s = ''.join([_val(tk) for tk in _filter(token.tokens)])
        s = s.replace('\n', ' ')
        return s

    if token.is_group() and len(token.tokens) > 1:

        if isinstance(token, Identifier):
            return ' '.join([tk.value for tk in _filter(token.tokens)])

        if isinstance(token, Comparison):
            return ' '.join([tk.value for tk in _filter(token.tokens)])

        if isinstance(token, IdentifierList):
            s = ' '.join([_val(tk) for tk in _filter(token.tokens)])
            return s.replace(' , ', ',\n' + ' ' * indent)

    return token.value


class _Formatter:

    TOKENS = ['SELECT', 'FROM', 'WHERE', ]
    TOKENS_BREAK = ['LEFT JOIN', 'AND', 'OR', 'JOIN', ]

    def __init__(self):
        self._lines = []
        self._line = []

    def _add_to_lines(self, indent):
        if self._line:
            row = '%s%s' % (indent * ' ', ' '.join(self._line))
            self._line = []
            self._lines.append(row)

    def _remove_white_before_semicolon(self):
        last_line = self._lines.pop()
        if last_line.endswith(' ;'):
            last_line = last_line.replace(' ;', ';')
        self._lines.append(last_line)

    def _tokens(self, sql):
        s = sqlparse.format(sql, keyword_case='upper')
        parsed = sqlparse.parse(s)[0]
        return _filter(parsed.tokens)

    def k(self, sql):
        tokens = self._tokens(sql)
        return self._format(tokens)

    def _format(self, tokens):
        indent = 4
        for token in tokens:
            if token.value in self.TOKENS:
                self._add_to_lines(indent)
                self._lines.append(token.value)
                continue

            if isinstance(token, Where):
                self._add_to_lines(indent)
                self._format(_filter(token.tokens))
                continue

            if token.value in self.TOKENS_BREAK:
                self._add_to_lines(indent)

            self._line.append(_val(token, indent))

        self._add_to_lines(indent)
        self._remove_white_before_semicolon()
        return '\n'.join(self._lines)


def format_sql(sql):
    formatter = _Formatter()
    return formatter.k(sql)
