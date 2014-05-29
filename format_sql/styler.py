# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from .parser import Comma, Compare, Identifier, Join, Key, Link, Sub


def _add_to_last_line(result, value, prefix=''):
    last = result.pop()
    if isinstance(last, list):
        _add_to_last_line(last, value, prefix)
        result.append(last)
    else:
        result.append('%s%s%s' % (prefix, last, value))


def _has_type(statement, classes):
    if statement:
        for cls in classes:
            if isinstance(statement, cls):
                return True
    return False


def _has_type_chain(statement, classes):
    for cls in classes:
        if not _has_type(statement, [cls]):
            return False
        statement = statement.statements[0]

    return True


def _style_statements(statement, last_statement, result):
    if not statement.statements:
        return

    sub = _style(statement.statements)

    if _has_type_chain(statement, [Compare, Sub]):
        _add_to_last_line(result, ' ' + sub.pop(0))
        sub = sub[0]

    if _has_type(last_statement, [Key]) and last_statement.value == 'ON':
        sub = [sub]

    result.append(sub)


def _style(statements):
    result = []
    last_statement = None
    on_prefix = ''
    for statement in statements:

        if on_prefix and _has_type(statement, [Join]):
            on_prefix = ''

        if _has_type(statement, [Identifier]) and _has_type(last_statement, [Sub]):
            _add_to_last_line(result, ' %s' % statement.value)

        elif _has_type(last_statement, [Link, Join]):
            _add_to_last_line(result, ' ' + statement.value)

        elif _has_type(last_statement, [Key]):
            if last_statement.value == 'ON':
                on_prefix = ' ' * 4
            _add_to_last_line(result, ' ' + statement.value, on_prefix)
        else:

            if _has_type(statement, [Comma]):
                _add_to_last_line(result, ',')
            else:
                result.append('%s%s' % (on_prefix, statement.value))

        _style_statements(statement, last_statement, result)

        if isinstance(statement, Sub):
            _add_to_last_line(result, ')')

        last_statement = statement

    return result


def _flatten(lists, indent=0):
    result = []
    for item in lists:
        if isinstance(item, list):
            result.append(_flatten(item, indent + 4))
        else:
            result.append(' ' * indent + item)
            result.append('\n')

    return ''.join(result)


def style(statements):
    styled = _style(statements)
    return _flatten(styled)
