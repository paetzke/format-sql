# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014-2015, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
import attr
from format_sql.tokenizer import Token


def _match(toks, types_list):
    if len(toks) < len(types_list):
        return False

    for tok, types in zip(toks, types_list):
        if types is None:
            continue
        if not isinstance(types, tuple):
            types = (types,)

        if tok._type not in types:
            return False

    return True


def _get_simple_object(tok, **kwargs):
    clazz = {
        Token.IDENTIFIER: Identifier,
        Token.NUMBER: Number,
        Token.STR: Str,
        Token.NOT: Not,
    }[tok._type]
    return clazz(tok._value, **kwargs)


class InvalidSQL(Exception):
    pass


class InvalidSelect(InvalidSQL):
    pass


class InvalidCondition(InvalidSQL):
    pass


class InvalidGroupBy(InvalidSQL):
    pass


class InvalidFunc(InvalidSQL):
    pass


class InvalidIdentifier(InvalidSQL):
    pass


class InvalidLimit(InvalidSQL):
    pass


class InvalidOrderBy(InvalidSQL):
    pass


class UnbalancedParenthesis(InvalidSQL):
    pass


@attr.s
class Identifier(object):
    value = attr.ib()
    alias = attr.ib(default=None)
    as_ = attr.ib(default=None)
    sort = attr.ib(default=None)

    def __str__(self):
        return '%s' % self.value


@attr.s
class Number(object):
    value = attr.ib()
    alias = attr.ib(default=None)
    as_ = attr.ib(default=None)
    sort = attr.ib(default=None)

    def __str__(self):
        return '%s' % self.value


@attr.s
class Str(object):
    value = attr.ib()
    alias = attr.ib(default=None)
    as_ = attr.ib(default=None)
    sort = attr.ib(default=None)

    def __str__(self):
        return '%s' % self.value


@attr.s
class Semicolon(object):
    value = attr.ib()


@attr.s
class Is(object):
    value = attr.ib()


@attr.s
class Null(object):
    value = attr.ib()


@attr.s
class GroupBy(object):
    values = attr.ib()
    with_rollup = attr.ib(default=None)


@attr.s
class From(object):
    value = attr.ib()
    values = attr.ib()


@attr.s
class Func(object):
    name = attr.ib()
    args = attr.ib()
    as_ = attr.ib(default=None)
    alias = attr.ib(default=None)


@attr.s
class Having(object):
    value = attr.ib()
    values = attr.ib()


@attr.s
class Join(object):
    value = attr.ib()


@attr.s
class Case(object):
    value = attr.ib()
    when_elses = attr.ib()


@attr.s
class When(object):
    when = attr.ib()
    condition = attr.ib()
    then = attr.ib()
    result = attr.ib()

    def __str__(self):
        return 'WHEN %s THEN %s' % (self.condition, self.result)


@attr.s
class Else(object):
    else_ = attr.ib()
    result = attr.ib()

    def __str__(self):
        return 'ELSE %s' % self.result


@attr.s
class Insert(object):
    insert = attr.ib()
    table = attr.ib()
    values = attr.ib(default=[])
    cols = attr.ib(default=[])
    select = attr.ib(default=[])


@attr.s
class Values(object):
    value = attr.ib()
    values = attr.ib()


@attr.s
class Limit(object):
    row_count = attr.ib()
    offset = attr.ib(default=None)
    offset_keyword = attr.ib(default=None)


@attr.s
class Link(object):
    value = attr.ib()


@attr.s
class Not(object):
    value = attr.ib()


@attr.s
class On(object):
    value = attr.ib()
    values = attr.ib(default=[])


@attr.s
class Between(object):
    value = attr.ib()


@attr.s
class Operator(object):
    value = attr.ib()

    def __str__(self):
        return '%s' % self.value.upper()


@attr.s
class OrderBy(object):
    values = attr.ib()


@attr.s
class Condition(object):
    values = attr.ib()


@attr.s
class Select(object):
    value = attr.ib()
    values = attr.ib()


@attr.s
class SubSelect(object):
    values = attr.ib()


@attr.s
class Where(object):
    value = attr.ib()
    conditions = attr.ib()


def _parse_func(toks):
    args = []
    if toks[0]._type != Token.FUNC:
        raise ValueError()
    if toks[1]._type != Token.PARENTHESIS_OPEN:
        raise UnbalancedParenthesis()

    i = 2
    while i < len(toks):
        if toks[i]._type in (Token.IDENTIFIER, Token.NUMBER, Token.STR):
            value = _get_simple_object(toks[i])
            args.append(value)
            i += 1
        elif toks[i]._type == Token.FUNC:
            func, j = _parse_func(toks[i:])
            args.append(func)
            i += j
        elif i != 2 and toks[i]._type != Token.PARENTHESIS_CLOSE:
            raise InvalidFunc()

        if toks[i]._type == Token.COMMA:
            i += 1
        elif toks[i]._type == Token.PARENTHESIS_CLOSE:
            i += 1
            break
        else:
            raise InvalidFunc()
    else:
        raise UnbalancedParenthesis()

    func = Func(toks[0]._value, args)

    alias, j = _parse_alias(toks[i:])
    i += j
    func.as_ = alias['as']
    func.alias = alias['alias']

    return func, i


def _parse_from(toks):
    i = 1
    values = []

    while len(toks) > i:
        if toks[i]._type in (Token.IDENTIFIER, Token.NUMBER):
            value, j = _parse_identifier(toks[i:])
            i += j
            values.append(value)

        elif toks[i]._type == Token.JOIN:
            join = Join(toks[i]._value)
            i += 1
            values.append(join)

        elif toks[i]._type == Token.ON:
            on = On(toks[i]._value)
            i += 1
            vals = []

            while len(toks) > i:
                if _match(toks[i:], [Token.IDENTIFIER, Token.COMPARE, Token.IDENTIFIER]):
                    condition = Condition([Identifier(toks[i + 0]._value),
                                           Operator(toks[i + 1]._value),
                                           Identifier(toks[i + 2]._value)])

                    vals.append(condition)
                    i += 3

                if _match(toks[i:], [Token.IDENTIFIER, Token.COMPARE, Token.FUNC]):
                    func, j = _parse_func(toks[i + 2:])
                    condition = Condition([Identifier(toks[i + 0]._value),
                                           Operator(toks[i + 1]._value),
                                           func])
                    vals.append(condition)
                    i += 2 + j

                if _match(toks[i:], [Token.FUNC]):
                    func, j = _parse_func(toks[i:])

                    if _match(toks[i + j:], [Token.COMPARE, Token.IDENTIFIER]):
                        i += j
                        condition = Condition([func,
                                               Operator(toks[i + 0]._value),
                                               Identifier(toks[i + 1]._value)])
                        vals.append(condition)
                        i += 2

                    elif _match(toks[i + j:], [Token.COMPARE, Token.FUNC]):
                        i += j
                        func2, j = _parse_func(toks[i + 1:])

                        condition = Condition([func,
                                               Operator(toks[i + 0]._value),
                                               func2])
                        vals.append(condition)
                        i += 2 + j

                if len(toks) <= i or toks[i]._type != Token.LINK:
                    break

                link = Link(toks[i]._value)
                vals.append(link)
                i += 1

            on.values = vals
            values.append(on)

        elif toks[i]._type == Token.COMMA:
            i += 1

        else:
            break

    from_ = From(toks[0]._value, values)
    return from_, i


def _parse_alias(toks):
    i = 0
    result = {'as': None, 'alias': None}
    if len(toks) > i and toks[i]._type == Token.AS:
        result['as'] = toks[i]._value
        i += 1

    if _match(toks[i:], [(Token.IDENTIFIER, Token.STR, Token.NUMBER)]):
        result['alias'] = toks[i]._value
        i += 1
    return result, i


def _parse_group_by(toks):
    values = []

    i = 1
    while i < len(toks):
        if toks[i]._type not in (Token.IDENTIFIER, Token.NUMBER):
            raise InvalidGroupBy()

        value = _get_simple_object(toks[i])
        values.append(value)
        i += 1

        if len(toks) > i and toks[i]._type == Token.COMMA:
            i += 1
        else:
            break

    with_rollup = None
    if len(toks) > i and toks[i]._type == Token.WITH_ROLLUP:
        with_rollup = toks[i]._value
        i += 1

    group_by = GroupBy(values, with_rollup=with_rollup)
    return group_by, i


def _parse_having(toks):
    conditions, j = _parse_conditions(toks[1:])
    having = Having(toks[0]._value, conditions)
    return having, j + 1


def _parse_limit(toks):
    if len(toks) > 3:

        if _match(toks, [Token.LIMIT, Token.NUMBER, Token.COMMA, Token.NUMBER]):
            return Limit(row_count=Number(toks[3]._value),
                         offset=Number(toks[1]._value)), 4

        if _match(toks, [Token.LIMIT, Token.NUMBER, Token.IDENTIFIER, Token.NUMBER]):
            if toks[2]._value.upper() == 'OFFSET':

                return Limit(row_count=Number(toks[1]._value),
                             offset=Number(toks[3]._value),
                             offset_keyword=toks[2]._value), 4

    if _match(toks, [Token.LIMIT, Token.NUMBER]):
        return Limit(row_count=Number(toks[1]._value)), 2

    raise InvalidLimit('%s' % toks)


def _parse_order_by(toks):
    values = []

    i = 1
    while i < len(toks):
        if not toks[i]._type in (Token.IDENTIFIER, Token.NUMBER):
            raise InvalidOrderBy()

        if _match(toks[i:], [None, (Token.ASC, Token.DESC)]):
            value = _get_simple_object(toks[i], sort=toks[i + 1]._value)
            values.append(value)
            i += 2
        else:
            value = _get_simple_object(toks[i])
            values.append(value)
            i += 1

        if _match(toks[i:], [Token.COMMA]):
            i += 1
        else:
            break

    return OrderBy(values), i


def _parse_insert(toks):
    assert toks[1]._type == Token.IDENTIFIER

    i = 2
    columns = []
    if toks[i]._type == Token.PARENTHESIS_OPEN:
        i += 1

        while i < len(toks):
            if toks[i]._type in (Token.NUMBER, Token.STR, Token.IDENTIFIER):
                columns.append(_get_simple_object(toks[i]))
                i += 1

            if toks[i]._type == Token.COMMA:
                i += 1
            elif toks[i]._type == Token.PARENTHESIS_CLOSE:
                i += 1
                break

    value_val = toks[i]._value
    select = []
    values = []
    if _match(toks[i:], [Token.VALUES, Token.PARENTHESIS_OPEN]):
        i += 2

        values_list = []
        while i < len(toks):

            if toks[i]._type in (Token.IDENTIFIER, Token.NUMBER, Token.STR):
                values.append(_get_simple_object(toks[i]))
                i += 1

            if toks[i]._type == Token.COMMA:
                i += 1

            elif _match(toks[i:], [Token.PARENTHESIS_CLOSE,
                                   Token.COMMA,
                                   Token.PARENTHESIS_OPEN]):
                values_list.append(values)
                values = []
                i += 3

            else:
                break

        assert toks[i]._type == Token.PARENTHESIS_CLOSE

        values_list.append(values)
        values = Values(value_val, values_list)

    elif toks[i]._type == Token.SELECT:
        for x, j in _parse(toks[i:]):
            select.append(x)
            i += j

    return Insert(toks[0]._value, toks[1]._value, values, cols=columns, select=select), i


def _parse_select(toks):
    values = []

    i = 1
    while i < len(toks):

        if toks[i]._type in (Token.IDENTIFIER, Token.NUMBER):
            value, j = _parse_identifier(toks[i:])
            values.append(value)
            i += j

        elif toks[i]._type == Token.FUNC:
            func, j = _parse_func(toks[i:])
            values.append(func)
            i += j

        elif toks[i]._type == Token.CASE:
            value, j = _parse_case(toks[i:])
            values.append(value)
            i += j

        else:
            raise InvalidSelect()

        if i > len(toks) - 1:
            break
        if toks[i]._type != Token.COMMA:
            break
        i += 1

    return Select(toks[0]._value, values), i


def _parse_case(toks):
    i = 1
    when_elses = []

    while i < len(toks):
        if _match(toks[i:], [
                Token.WHEN,
                (Token.IDENTIFIER, Token.NUMBER, Token.STR),
                Token.THEN,
                (Token.IDENTIFIER, Token.NUMBER, Token.STR)]):

            when = When(toks[i + 0]._value,
                        toks[i + 1]._value,
                        toks[i + 2]._value,
                        toks[i + 3]._value,)
            when_elses.append(when)
            i += 4

        elif _match(toks[i:], [
                Token.ELSE,
                (Token.IDENTIFIER, Token.NUMBER, Token.STR)]):

            else_ = Else(toks[i + 0]._value,
                         toks[i + 1]._value)
            when_elses.append(else_)
            i += 2

        else:
            break

    return Case(toks[0]._value, when_elses), i


def _parse_semicolon(toks):
    return Semicolon(';'), 1


def _parse_where(toks):
    conditions, j = _parse_conditions(toks[1:])
    where = Where(toks[0]._value, conditions)
    return where, j + 1


def _parse_conditions(toks):
    conditions = []

    i = 0
    while i < len(toks):

        if _match(toks[i:], [Token.NOT,
                             (Token.IDENTIFIER, Token.NUMBER, Token.STR),
                             Token.COMPARE,
                             (Token.IDENTIFIER, Token.NUMBER, Token.STR)]):

            condition = Condition([Not(toks[i]._value),
                                   _get_simple_object(toks[i + 1]),
                                   Operator(toks[i + 2]._value),
                                   _get_simple_object(toks[i + 3])])
            conditions.append(condition)
            i += 4
        elif _match(toks[i:], [(Token.IDENTIFIER, Token.NUMBER, Token.STR),
                               Token.BETWEEN,
                               (Token.IDENTIFIER, Token.NUMBER, Token.STR),
                               Token.LINK,
                               (Token.IDENTIFIER, Token.NUMBER, Token.STR)]):
            condition = Condition([
                _get_simple_object(toks[i]),
                Between(toks[i + 1]._value),
                _get_simple_object(toks[i + 2]),
                Link(toks[i + 3]._value),
                _get_simple_object(toks[i + 4])
            ])
            conditions.append(condition)
            i += 5

        elif _match(toks[i:], [(Token.IDENTIFIER, Token.NUMBER, Token.STR),
                               Token.COMPARE,
                               (Token.IDENTIFIER, Token.NUMBER, Token.STR)]):
            condition = Condition([_get_simple_object(toks[i]),
                                   Operator(toks[i + 1]._value),
                                   _get_simple_object(toks[i + 2])])
            conditions.append(condition)
            i += 3

        elif _match(toks[i:], [(Token.IDENTIFIER, Token.NUMBER, Token.STR),
                               Token.IS,
                               Token.NULL]):
            condition = Condition([_get_simple_object(toks[i]),
                                   Is(toks[i + 1]._value),
                                   Null(toks[i + 2]._value)])
            conditions.append(condition)
            i += 3

        elif _match(toks[i:], [(Token.IDENTIFIER, Token.NUMBER, Token.STR),
                               Token.IS,
                               Token.NOT,
                               Token.NULL]):
            condition = Condition([_get_simple_object(toks[i]),
                                   Is(toks[i + 1]._value),
                                   Not(toks[i + 2]._value),
                                   Null(toks[i + 3]._value)])
            conditions.append(condition)
            i += 4

        elif _match(toks[i:], [Token.NOT, Token.FUNC, None, None, None, None]):
            func, j = _parse_func(toks[i + 1:])
            condition = Condition([Not(toks[i]._value),
                                   func,
                                   Operator(toks[i + j + 1]._value),
                                   _get_simple_object(toks[i + j + 2])])
            conditions.append(condition)
            i += j

        elif _match(toks, [(Token.IDENTIFIER, Token.NUMBER),
                           (Token.IN, Token.COMPARE),
                           Token.PARENTHESIS_OPEN,
                           None,
                           None]):
            condition = Condition([_get_simple_object(toks[i]),
                                   Operator(toks[i + 1]._value)])
            i += 3
            objects = []

            while toks[i]._type != Token.PARENTHESIS_CLOSE:
                if toks[i]._type in (Token.NUMBER, Token.STR, Token.IDENTIFIER):
                    value = _get_simple_object(toks[i])
                    objects.append(value)
                    i += 1
                if toks[i]._type == Token.COMMA:
                    i += 1

                if toks[i]._type == Token.SELECT:
                    values = []
                    for x, j in _parse(toks[i:]):
                        values.append(x)
                        i += j
                    objects = SubSelect(values)

            i += 1
            condition.values.append(objects)
            conditions.append(condition)

        else:
            raise InvalidCondition()

        if len(toks) <= i or toks[i]._type != Token.LINK:
            break
        link = Link(toks[i]._value)
        conditions.append(link)
        i += 1

    return conditions, i


def _parse_identifier(toks):
    count = 0

    if _match(toks, [(Token.IDENTIFIER, Token.STR, Token.NUMBER)]):
        if toks[0]._type == Token.IDENTIFIER:
            cls = Identifier
        elif toks[0]._type == Token.NUMBER:
            cls = Number

        value = cls(toks[0]._value)
        count += 1

        alias, j = _parse_alias(toks[count:])
        count += j
        value.as_ = alias['as']
        value.alias = alias['alias']

        return value, count

    raise InvalidIdentifier(toks)


def _parse(toks):
    structures = {
        Token.GROUP_BY: _parse_group_by,
        Token.FROM: _parse_from,
        Token.FUNC: _parse_func,
        Token.HAVING: _parse_having,
        Token.INSERT: _parse_insert,
        Token.LIMIT: _parse_limit,
        Token.ORDER_BY: _parse_order_by,
        Token.SELECT: _parse_select,
        Token.SEMICOLON: _parse_semicolon,
        Token.WHERE: _parse_where,
    }

    while toks:
        if toks[0]._type == Token.PARENTHESIS_CLOSE:
            raise StopIteration

        try:
            func = structures[toks[0]._type]
        except KeyError:
            raise InvalidSQL()
        statement, count = func(toks)
        toks = toks[count:]
        yield statement, count


def parse(toks):
    for statement, unused_count in _parse(toks):
        yield statement
