# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
import re
from itertools import chain

import sqlparse

ADDITIONAL = ['FROM', 'WHERE', 'LIMIT', 'GROUP BY', 'HAVING', 'ORDER BY']
COMPARES = ('=', 'IN', '<>', '>', '<',  '!=', 'IS')
JOINS = ('JOIN', 'INNER JOIN', 'FULL OUTER JOIN', 'LEFT OUTER JOIN',
         'LEFT JOIN',  'RIGHT OUTER JOIN', 'RIGHT JOIN')
KEYWORDS = ('ON', 'NULL', 'NOT')
LINKS = ('AND', 'OR')
SELECTS = ('SELECT DISTINCT', 'SELECT SQL_NO_CACHE', 'SELECT')
STRS = [
    r'\w+\(.*?\)',
    r'".*?"',
    r'[\w\d%]+\([_\w\d\.`%]+\)[\w\d]*',
    r'[_\w\d\.`%]+',
    r"'.*?'"
]
PUNCTUATIONS = [r',', r'\)', r'\(']
IGNORABLE = ['\s+', '.+?']

CHAINED = chain(JOINS, SELECTS, ADDITIONAL, PUNCTUATIONS,
                COMPARES, LINKS, KEYWORDS, STRS, IGNORABLE)
TOKENS_RE = re.compile('|'.join('(%s)' % x for x in CHAINED))


class Type:
    COMPARE = 'COMPARE'
    FROM = 'FROM'
    GROUP = 'GROUP'
    HAVING = 'HAVING'
    JOIN = 'JOIN'
    KEYWORD = 'KEYWORD'
    LIMIT = 'LIMIT'
    LINK = 'LINK'
    PUNCTUATION = 'PUNCTUATION'
    SELECT = 'SELECT'
    STR = 'STR'
    WHERE = 'WHERE'
    ORDER = 'ORDER'


class Token:

    def __init__(self, token_type, value):
        self._type = token_type
        self.value = value

    def __str__(self):
        return '<Token %s: %s>' % (self._type, self.value)

    def is_closing_parenthesis(self):
        return self._type == Type.PUNCTUATION and self.value == ')'

    def is_opening_parenthesis(self):
        return self._type == Type.PUNCTUATION and self.value == '('

    def is_comma(self):
        return self._type == Type.PUNCTUATION and self.value == ','

    @classmethod
    def from_value(cls, value):
        if not value.strip():
            return None

        try:
            token_type = {
                'FROM': Type.FROM,
                'GROUP BY': Type.GROUP,
                'HAVING': Type.HAVING,
                'LIMIT': Type.LIMIT,
                'ORDER BY': Type.ORDER,
                'WHERE': Type.WHERE,
            }[value]
            return cls(token_type, value)
        except KeyError:
            pass

        token_types = {
            COMPARES: Type.COMPARE,
            JOINS: Type.JOIN,
            KEYWORDS: Type.KEYWORD,
            LINKS: Type.LINK,
            SELECTS: Type.SELECT,
            (',', '(', ')'): Type.PUNCTUATION,
        }

        for values, token_type in token_types.items():
            if value in values:
                return cls(token_type, value)

        return cls(Type.STR, value)


def normalize_sql(sql_str):
    normalized = sqlparse.format(sql_str, keyword_case='upper')
    has_semicolon = normalized.endswith(';')
    if has_semicolon:
        normalized = normalized[:-1]
    return str(normalized), has_semicolon


def _create_str_token(str_tokens):
    return Token(Type.STR, value=' '.join(tk.value for tk in str_tokens))


def _merge_str_tokens(tokens):
    str_tokens = []

    for token in tokens:
        if token._type == Type.STR:
            str_tokens.append(token)
        else:
            if str_tokens:
                yield _create_str_token(str_tokens)
                str_tokens = []
            yield token

    if str_tokens:
        yield _create_str_token(str_tokens)


def _tokenize(sql_str):
    scanner = TOKENS_RE.scanner(sql_str)
    for m in iter(scanner.match, None):
        token = Token.from_value(m.group())
        if token:
            yield token


def tokenize(sql_str):
    tokens = _tokenize(sql_str)
    return list(_merge_str_tokens(tokens))
