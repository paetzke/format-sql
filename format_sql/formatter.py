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
    return [token for token in tokens if not token.is_whitespace()]


def _val(token, indent=0):
    if isinstance(token, Parenthesis):
        tokens = list(_filter(token.tokens))[1:-1]
        if tokens[0].is_keyword:
            fort = _Formatter()
            return '(\n%s)' % fort._make_it_so(tokens=tokens, indent=indent + 4)
        else:
            vals = [_val(tk) for tk in _filter(token.tokens)]
            s = ''.join(vals)
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
    TOKENS_BREAK = [
        ('LEFT JOIN', 0),
        ('AND', 0),
        ('OR', 0),
        ('JOIN', 0),
        ('GROUP BY', 1),
        ('HAVING', 0),
    ]

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

    def _make_it_so(self, sql=None, tokens=None, indent=0):
        if not tokens:
            tokens = self._tokens(sql)
        return self._format(tokens, indent=indent)

    def _format(self, tokens, indent=0):
        i = -1
        while i + 1 < len(tokens):
            i += 1
            token = tokens[i]

            if token.value in self.TOKENS:
                self._add_to_lines(indent + 4)
                self._line.append(token.value)
                self._add_to_lines(indent)
                continue

            if isinstance(token, Where):
                self._add_to_lines(indent + 4)
                self._format(_filter(token.tokens))
                continue

            in_break, k, s = self._in_break_tokens(tokens[i:])
            if in_break:
                self._add_to_lines(indent + 4)
                self._line.append(s)
                i += k
                if s in ('GROUP BY', 'HAVING'):
                    self._add_to_lines(indent)
                continue

            self._line.append(_val(token, indent + 4))

        self._add_to_lines(indent + 4)
        self._remove_white_before_semicolon()
        return '\n'.join(self._lines)

    def _in_break_tokens(self, tokens):
        for token_value, tokens_len in self.TOKENS_BREAK:
            tks = ' '.join(tk.value for tk in tokens[:tokens_len + 1])
            if tks == token_value:
                return True, tokens_len, token_value
        return False, 0, ''


def format_sql(sql):
    formatter = _Formatter()
    return formatter._make_it_so(sql)
