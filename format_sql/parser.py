# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from .tokenizer import Type


class Statement:

    def __init__(self, value, statements=[]):
        self.value = value
        self.statements = statements

    def __str__(self):
        return '%s-%s' % (self.__class__, self.value)


class Comma(Statement):
    pass


class Compare(Statement):
    pass


class From(Statement):
    pass


class Group(Statement):
    pass


class Having(Statement):
    pass


class Join(Statement):
    pass


class Key(Statement):
    pass


class Limit(Statement):
    pass


class Link(Statement):
    pass


class Order(Statement):
    pass


class Select(Statement):
    pass


class Sub(Statement):
    pass


class Where(Statement):
    pass


class Identifier(Statement):
    pass


def _cls_with_sub_statements(cls, token, sub_tokens, nested=True):
    sub_statements, count = _parse(sub_tokens, nested)
    statement = cls(token.value, statements=sub_statements)
    return statement,  count


def _cls_from_dict(token, sub_tokens):
    statements_with_subs = {
        Type.SELECT: Select,
        Type.FROM: From,
        Type.GROUP: Group,
        Type.HAVING: Having,
        Type.LIMIT: Limit,
        Type.ORDER: Order,
        Type.WHERE: Where,
    }

    statements_without_subs = {
        Type.JOIN: Join,
        Type.KEYWORD: Key,
        Type.LINK: Link,
    }

    statement, count = None, 0
    try:
        cls = statements_with_subs[token._type]
        statement, count = _cls_with_sub_statements(cls, token, sub_tokens)
    except KeyError:
        try:
            cls = statements_without_subs[token._type]
            statement = cls(token.value)
        except KeyError:
            pass

    return statement, count + 1


def _parse(tokens, nested=False):
    statements = []

    if not tokens:
        return statements, 0

    i = 0
    while i < len(tokens):
        # Py3k: token, *sub_tokens
        token, sub_tokens = tokens[i], tokens[i + 1:]

        if nested and token._type in [Type.FROM, Type.GROUP, Type.HAVING,
                                      Type.LIMIT, Type.ORDER, Type.WHERE]:
            break
        if token.is_closing_parenthesis():
            break

        statement, count = _cls_from_dict(token, sub_tokens)
        if statement:
            i += count

        elif token._type == Type.STR:
            if sub_tokens and sub_tokens[0]._type == Type.COMPARE:
                is_list_compare = sub_tokens[1]._type == Type.PUNCTUATION
                if is_list_compare:
                    tks = [token, sub_tokens[0]]
                    sub_statement, count = _parse(sub_tokens[1:], nested=True)
                else:
                    tks = [token, sub_tokens[0], sub_tokens[1]]

                value = ' '.join(tk.value for tk in tks)
                statement = Compare(value)

                if is_list_compare:
                    statement.statements = sub_statement
                    i += count

                i += len(tks)
            else:
                statement = Identifier(token.value)
                i += 1

        elif token.is_opening_parenthesis():
            statement, count = _cls_with_sub_statements(Sub, token, sub_tokens,
                                                        nested=False)
            i += 2 + count

        elif token.is_comma():
            statement = Comma(token.value)
            i += 1

        statements.append(statement)

    return statements, i


def parse(tokens):
    statements, _unused_token_count = _parse(tokens)
    return statements
