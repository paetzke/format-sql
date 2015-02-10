# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014-2015, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from format_sql.tokenizer import Token


def _get_simple_object(token, **kwargs):
    if token._type == Token.IDENTIFIER:
        return Identifier(token._value, **kwargs)
    if token._type == Token.NUMBER:
        return Number(token._value, **kwargs)
    if token._type == Token.STR:
        return Str(token._value, **kwargs)
    if token._type == Token.NOT:
        return Not(token._value)
    raise ValueError()


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


class SingleValue:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.value == other.value


class SingleAndListValue:

    def __init__(self, value, values=[]):
        self.value = value
        self.values = values

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and all([self.value == other.value,
                     self.values == other.values])


class Value:

    def __init__(self, value, alias=None, as_=None, **kwargs):
        self.value = value
        self.alias = alias
        self.as_ = as_
        self.kwargs = kwargs

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and all([self.value == other.value,
                     self.alias == other.alias,
                     self.as_ == other.as_,
                     self.kwargs == other.kwargs])

    def __str__(self):
        return '%s' % self.value


class Identifier(Value):

    def __repr__(self):
        return 'Identifier(%s)' % self.value


class Number(Value):

    def __repr__(self):
        return 'Number(%s)' % self.value


class Str(Value):

    def __repr__(self):
        return 'Str(%s)' % self.value


class Semicolon(Value):
    name = 'SEMICOLON'

    def __repr__(self):
        return 'Semicolon(%s)' % self.value


class GroupBy:
    name = 'GROUP BY'

    def __init__(self, values, with_rollup=None):
        self.values = values
        self.with_rollup = with_rollup

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and all([self.values == other.values,
                     self.with_rollup == other.with_rollup])

    def __repr__(self):
        return 'GroupBy(with_rollup=%s, values=%s)' % (self.with_rollup, self.values)


class From(SingleAndListValue):
    name = 'FROM'

    def __repr__(self):
        return 'From(%s, values=%s)' % (self.value, self.values)


class Func:
    name = 'FUNC'

    def __init__(self, name, args, as_=None, alias=None):
        self.name = name
        self.args = args
        self.as_ = as_
        self.alias = alias

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and all([self.name == other.name,
                     self.args == other.args,
                     self.as_ == other.as_,
                     self.alias == other.alias])


class Having:
    name = 'HAVING'

    def __init__(self, value, values):
        self.value = value
        self.values = values

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and all([self.value == other.value,
                     self.values == other.values])

    def __repr__(self):
        return 'Having(%s, %s)' % (self.value, self.values)


class Join(SingleValue):

    def __repr__(self):
        return 'Join(%s)' % self.value


class Limit:
    name = 'LIMIT'

    def __init__(self, row_count, offset=None, offset_keyword=None):
        self.row_count = row_count
        self.offset = offset
        self.offset_keyword = offset_keyword

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and all([self.row_count == other.row_count,
                     self.offset == other.offset,
                     self.offset_keyword == other.offset_keyword])

    def __repr__(self):
        return 'Limit(row_count=%s, offset=%s)' % (self.row_count, self.offset)


class Link(SingleValue):
    name = 'LINK'

    def __repr__(self):
        return 'Link(%s)' % self.value

    def __str__(self):
        return '%s' % self.value


class Not(SingleValue):
    name = 'NOT'


class On(SingleAndListValue):
    name = 'ON'

    def __repr__(self):
        return 'On(%s, %s)' % (self.value, self.values)


class Operator(SingleValue):
    name = 'OPERATOR'

    def __repr__(self):
        return 'Operator(%s)' % self.value

    def __str__(self):
        return '%s' % self.value


class OrderBy:
    name = 'ORDER BY'

    def __init__(self, values):
        self.values = values

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.values == other.values

    def __repr__(self):
        return 'OrderBy(values=%s)' % self.values


class Condition:
    name = 'condition'

    def __init__(self, values):
        self.values = values

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.values == other.values

    def __repr__(self):
        return 'Condition(%s)' % self.values


class Select(SingleAndListValue):
    name = 'SELECT'

    def __repr__(self):
        return 'Select(%s, %s)' % (self.value, self.values)


class SubSelect:

    def __init__(self, values=[]):
        self.values = values

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.values == other.values


class Where:
    name = 'WHERE'

    def __init__(self, value, conditions):
        self.value = value
        self.conditions = conditions

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and all([self.value == other.value,
                     self.conditions == other.conditions])

    def __repr__(self):
        return 'Where(%s, %s)' % (self.value, self.conditions)


def _parse_func(tokens):
    args = []
    if tokens[0]._type != Token.FUNC:
        raise ValueError()
    if tokens[1]._type != Token.PARENTHESIS_OPEN:
        raise UnbalancedParenthesis()

    i = 2
    while i < len(tokens):
        if tokens[i]._type in (Token.IDENTIFIER, Token.NUMBER, Token.STR):
            value = _get_simple_object(tokens[i])
            args.append(value)
            i += 1
        elif tokens[i]._type == Token.FUNC:
            func, j = _parse_func(tokens[i:])
            args.append(func)
            i += j
        else:
            raise InvalidFunc()

        if tokens[i]._type == Token.COMMA:
            i += 1
        elif tokens[i]._type == Token.PARENTHESIS_CLOSE:
            i += 1
            break
        else:
            raise InvalidFunc()
    else:
        raise UnbalancedParenthesis()

    func = Func(tokens[0]._value, args)

    alias, j = _parse_alias(tokens[i:])
    i += j
    func.as_ = alias['as']
    func.alias = alias['alias']

    return func, i


def _parse_from(tokens):
    i = 1
    values = []

    while len(tokens) > i:
        if tokens[i]._type in (Token.IDENTIFIER, Token.NUMBER):
            value, j = _parse_identifier(tokens[i:])
            i += j
            values.append(value)

        elif tokens[i]._type == Token.JOIN:
            join = Join(tokens[i]._value)
            i += 1
            values.append(join)

        elif tokens[i]._type == Token.ON:
            on = On(tokens[i]._value)
            i += 1
            vals = []

            while len(tokens) > i:
                if len(tokens) > 2 + i and all([
                        tokens[i + 0]._type == Token.IDENTIFIER,
                        tokens[i + 1]._type == Token.COMPARE,
                        tokens[i + 2]._type == Token.IDENTIFIER]):

                    condition = Condition([Identifier(tokens[i + 0]._value),
                                           Operator(tokens[i + 1]._value),
                                           Identifier(tokens[i + 2]._value)])

                    vals.append(condition)
                    i += 3

                if len(tokens) <= i or tokens[i]._type != Token.LINK:
                    break

                link = Link(tokens[i]._value)
                vals.append(link)
                i += 1

            on.values = vals
            values.append(on)

        elif tokens[i]._type == Token.COMMA:
            i += 1

        else:
            break

    from_ = From(tokens[0]._value, values)
    return from_, i


def _parse_alias(tokens):
    i = 0
    result = {'as': None, 'alias': None}
    if len(tokens) > i and tokens[i]._type == Token.AS:
        result['as'] = tokens[i]._value
        i += 1

    if len(tokens) > i and tokens[i]._type in (Token.IDENTIFIER,
                                               Token.STR,
                                               Token.NUMBER):
        result['alias'] = tokens[i]._value
        i += 1
    return result, i


def _parse_group_by(tokens):
    values = []

    i = 1
    while i < len(tokens):
        if tokens[i]._type not in (Token.IDENTIFIER, Token.NUMBER):
            raise InvalidGroupBy()

        value = _get_simple_object(tokens[i])
        values.append(value)
        i += 1

        if len(tokens) > i and tokens[i]._type == Token.COMMA:
            i += 1
        else:
            break

    with_rollup = None
    if len(tokens) > i and tokens[i]._type == Token.WITH_ROLLUP:
        with_rollup = tokens[i]._value
        i += 1

    group_by = GroupBy(values, with_rollup=with_rollup)
    return group_by, i


def _parse_having(tokens):
    conditions, j = _parse_conditions(tokens[1:])
    having = Having(tokens[0]._value, conditions)
    return having, j + 1


def _parse_limit(tokens):
    if len(tokens) > 3:
        if all([tokens[0]._type == Token.LIMIT,
                tokens[1]._type == Token.NUMBER,
                tokens[2]._type == Token.COMMA,
                tokens[3]._type == Token.NUMBER]):

            return Limit(row_count=Number(tokens[3]._value),
                         offset=Number(tokens[1]._value)), 4

        if all([tokens[0]._type == Token.LIMIT,
                tokens[1]._type == Token.NUMBER,
                tokens[2]._type == Token.IDENTIFIER,
                tokens[2]._value.upper() == 'OFFSET',
                tokens[3]._type == Token.NUMBER]):

            return Limit(row_count=Number(tokens[1]._value),
                         offset=Number(tokens[3]._value),
                         offset_keyword=tokens[2]._value), 4

    if len(tokens) > 1 and all([tokens[0]._type == Token.LIMIT,
                                tokens[1]._type == Token.NUMBER]):
        return Limit(row_count=Number(tokens[1]._value)), 2

    raise InvalidLimit('%s' % tokens)


def _parse_order_by(tokens):
    values = []

    i = 1
    while i < len(tokens):
        if not tokens[i]._type in (Token.IDENTIFIER, Token.NUMBER):
            raise InvalidOrderBy()

        if len(tokens) > i + 1 and tokens[i + 1]._type in (Token.ASC, Token.DESC):
            value = _get_simple_object(tokens[i], sort=tokens[i + 1]._value)
            values.append(value)
            i += 2
        else:
            value = _get_simple_object(tokens[i])
            values.append(value)
            i += 1

        if len(tokens) > i and tokens[i]._type == Token.COMMA:
            i += 1
        else:
            break

    return OrderBy(values), i


def _parse_select(tokens):
    values = []

    i = 1
    while i < len(tokens):

        if tokens[i]._type in (Token.IDENTIFIER, Token.NUMBER):
            value, j = _parse_identifier(tokens[i:])
            values.append(value)
            i += j
        elif tokens[i]._type == Token.FUNC:
            func, j = _parse_func(tokens[i:])
            values.append(func)
            i += j
        else:
            raise InvalidSelect()

        if i > len(tokens) - 1:
            break
        if tokens[i]._type != Token.COMMA:
            break
        i += 1

    return Select(tokens[0]._value, values), i


def _parse_semicolon(tokens):
    return Semicolon(';'), 1


def _parse_where(tokens):
    conditions, j = _parse_conditions(tokens[1:])
    where = Where(tokens[0]._value, conditions)
    return where, j + 1


def _parse_conditions(tokens):
    conditions = []

    i = 0
    while i < len(tokens):
        if len(tokens) > 3 + i and all([
                tokens[i + 0]._type == Token.NOT,
                tokens[
                    i + 1]._type in (Token.IDENTIFIER, Token.NUMBER, Token.STR),
                tokens[i + 2]._type == Token.COMPARE,
                tokens[i + 3]._type in (Token.IDENTIFIER, Token.NUMBER, Token.STR)]):

            condition = Condition([Not(tokens[i]._value),
                                   _get_simple_object(tokens[i + 1]),
                                   Operator(tokens[i + 2]._value),
                                   _get_simple_object(tokens[i + 3])])
            conditions.append(condition)
            i += 4

        elif len(tokens) > 2 + i and all([
                tokens[
                    i + 0]._type in (Token.IDENTIFIER, Token.NUMBER, Token.STR),
                tokens[i + 1]._type == Token.COMPARE,
                tokens[i + 2]._type in (Token.IDENTIFIER, Token.NUMBER, Token.STR)]):

            condition = Condition([_get_simple_object(tokens[i]),
                                   Operator(tokens[i + 1]._value),
                                   _get_simple_object(tokens[i + 2])])
            conditions.append(condition)
            i += 3

        elif len(tokens) > 5 + i and all([
                tokens[i + 0]._type == Token.NOT,
                tokens[i + 1]._type in Token.FUNC]):

            func, j = _parse_func(tokens[i + 1:])
            condition = Condition([Not(tokens[i]._value),
                                   func,
                                   Operator(tokens[i + j + 1]._value),
                                   _get_simple_object(tokens[i + j + 2])])
            conditions.append(condition)
            i += j

        elif len(tokens) > 4 + i and all([
                tokens[i + 0]._type in (Token.IDENTIFIER, Token.NUMBER),
                tokens[i + 1]._type in (Token.IN, Token.COMPARE),
                tokens[i + 2]._type == Token.PARENTHESIS_OPEN]):

            condition = Condition([_get_simple_object(tokens[i]),
                                   Operator(tokens[i + 1]._value)])
            i += 3
            objects = []

            while tokens[i]._type != Token.PARENTHESIS_CLOSE:
                if tokens[i]._type in (Token.NUMBER, Token.STR, Token.IDENTIFIER):
                    value = _get_simple_object(tokens[i])
                    objects.append(value)
                    i += 1
                if tokens[i]._type == Token.COMMA:
                    i += 1

                if tokens[i]._type == Token.SELECT:
                    values = []
                    for x, j in _parse(tokens[i:]):
                        values.append(x)
                        i += j
                    objects = SubSelect(values)

            i += 1
            condition.values.append(objects)
            conditions.append(condition)

        else:
            raise InvalidCondition()

        if len(tokens) <= i or tokens[i]._type != Token.LINK:
            break
        link = Link(tokens[i]._value)
        conditions.append(link)
        i += 1

    return conditions, i


def _parse_identifier(tokens):
    count = 0
    if len(tokens) > 0 and tokens[0]._type in (Token.IDENTIFIER,
                                               Token.STR,
                                               Token.NUMBER):
        if tokens[0]._type == Token.IDENTIFIER:
            cls = Identifier
        elif tokens[0]._type == Token.NUMBER:
            cls = Number

        value = cls(tokens[0]._value)
        count += 1

        alias, j = _parse_alias(tokens[count:])
        count += j
        value.as_ = alias['as']
        value.alias = alias['alias']

        return value, count

    raise InvalidIdentifier(tokens)


def _parse(tokens):
    structures = {
        Token.GROUP_BY: _parse_group_by,
        Token.FROM: _parse_from,
        Token.FUNC: _parse_func,
        Token.HAVING: _parse_having,
        Token.LIMIT: _parse_limit,
        Token.ORDER_BY: _parse_order_by,
        Token.SELECT: _parse_select,
        Token.SEMICOLON: _parse_semicolon,
        Token.WHERE: _parse_where,
    }

    while tokens:
        if tokens[0]._type == Token.PARENTHESIS_CLOSE:
            raise StopIteration

        try:
            func = structures[tokens[0]._type]
        except KeyError:
            raise InvalidSQL()
        statement, count = func(tokens)
        tokens = tokens[count:]
        yield statement, count


def parse(tokens):
    for statement, unused_count in _parse(tokens):
        yield statement
