# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
import re
from collections import OrderedDict


class StringNotTerminated(Exception):
    pass


class Token:
    AS = 'AS'
    ASC = 'ASC'
    COMMA = ','
    COMPARE = 'compare'
    DESC = 'DESC'
    FROM = 'FROM'
    FUNC = 'func'
    GROUP_BY = 'GROUP'
    IDENTIFIER = 'identifier'
    IN = 'IN'
    ON = 'ON'
    HAVING = 'HAVING'
    JOIN = 'join'
    LIMIT = 'LIMIT'
    LINK = 'link'
    NOT = 'NOT'
    NUMBER = 'number'
    ORDER_BY = 'ORDER'
    PARENTHESIS_CLOSE = ')'
    PARENTHESIS_OPEN = '('
    SEMICOLON = ';'
    SELECT = 'SELECT'
    STR = 'str'
    WITH_ROLLUP = 'WITH'
    WHERE = 'WHERE'

    def __init__(self, token_type, token_value):
        self._type = token_type
        self._value = token_value

    def __repr__(self):
        return '<%s: %s>' % (self._type, self._value)

    @staticmethod
    def get_token(value):
        normalized = value.split()[0].upper()

        if normalized in TOKEN_RES.keys():
            return normalized

        normalized = value.split()[-1].upper()
        if normalized == 'JOIN':
            return Token.JOIN

        return None


TOKEN_RES = OrderedDict([
    (Token.IN, [r'\bin\b']),
    (Token.ON, [r'\bon\b']),
    (Token.ASC, [r'\basc\b']),
    (Token.AS, [r'\bas\b']),
    (Token.SEMICOLON, [r';']),
    (Token.COMMA, [r',']),
    (Token.COMPARE, [r'=', r'!=', r'>=', r'<=', r'<>', r'<', r'>']),
    (Token.DESC, [r'\bdesc\b']),
    (Token.FROM, [r'\bfrom\b']),
    (Token.GROUP_BY, [r'\bgroup\s+by']),
    (Token.HAVING, [r'\bhaving\b']),
    (Token.SELECT, [r'\bselect\s+distinct\b',
                    r'\bselect\s+sql_no_cache\b',
                    r'\bselect\b']),
    (Token.LIMIT, [r'\blimit\b']),
    (Token.LINK, [r'\band\b', r'\bor\b']),
    (Token.NOT, [r'\bnot\b']),
    (Token.ORDER_BY, [r'\border\s+by\b']),
    (Token.PARENTHESIS_CLOSE, [r'\(']),
    (Token.PARENTHESIS_OPEN, [r'\)']),
    (Token.WITH_ROLLUP, [r'\bwith\s+rollup\b']),
    (Token.WHERE, [r'\bwhere\b']),
    (Token.FUNC, [r'\b\w+\b\s*\(']),
    (Token.JOIN, [r'\bleft\s+outer\s+join\b', r'\bleft\s+join\b',
                  r'\bright\s+outer\s+join\b', r'\bright\s+join\b',
                  r'\bnatural\s+join\b', r'\binner\s+join\b',
                  r'\bjoin\b']),
])


token_res = []
for res in TOKEN_RES.values():
    token_res.extend(res)


token_res.append(r'[-+]?\d+\.?\d*')
token_res.append(r'`\w+`\.`\w+`')  # `t1`.`t2`
token_res.append(r'`\w+`')
token_res.append(r'\b\w+\.\w+\b')
token_res.append(r'\b\w+\.\*')
token_res.append(r'\b\w+\b')

token_res.append(r'%\(\w+\)s')  # %(arg)s
token_res.append(r'%s')  # %s
token_res.append(r'\*')


reg_ex = r'|'.join(r'(%s)' % s for s in token_res)
sql_re = re.compile(reg_ex, re.IGNORECASE)


STR_STARTERS = ('"', "'")


def cutter(s):
    while s:
        if s.startswith(STR_STARTERS):
            starter = s[0]
            for i, c in enumerate(s[1:]):
                if c == starter:
                    value = s[:i + 2]
                    offset = len(value)
                    yield value
                    break
            else:
                raise StringNotTerminated(s)
        else:

            match = sql_re.match(s)
            if match:
                value = match.group(0)
                offset = len(value)
                yield value
            else:
                offset = 1

        s = s[offset:]


def tokenize(s):
    for word in cutter(s):
        token_type = Token.get_token(word)
        if token_type:
            yield Token(token_type, word)
        elif word[0].isdigit() or word.startswith(('+', '-')):
            yield Token(Token.NUMBER, word)
        elif word.endswith('('):
            yield Token(Token.FUNC, word[:-1].strip())
            yield Token(Token.PARENTHESIS_OPEN, '(')
        elif word.startswith(STR_STARTERS):
            yield Token(Token.STR, word)
        elif word in ('=', '<>', '<', '>', '!=', '>=', '<='):
            yield Token(Token.COMPARE, word)
        elif word.upper() in ('AND', 'OR'):
            yield Token(Token.LINK, word)
        else:
            yield Token(Token.IDENTIFIER, word)
