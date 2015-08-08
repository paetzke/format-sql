# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014-2015, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from format_sql.parser import (Identifier, InvalidCondition, InvalidIdentifier,
                               InvalidLimit, Number, _parse_identifier, parse)
from format_sql.tokenizer import Token

import pytest


def assert_statements(tokens1, statements2):
    parsed_statements = list(parse(tokens1))
    assert parsed_statements == statements2


@pytest.mark.parametrize(('tokens', 'exception'), [
    ([Token(Token.LIMIT, '')], InvalidLimit),
    ([Token(Token.WHERE, ''), Token(Token.IDENTIFIER, '')], InvalidCondition),
])
def test_parse_exceptions(tokens, exception):
    with pytest.raises(exception):
        list(parse(tokens))


def test_parse_identifier_with_exception():
    with pytest.raises(InvalidIdentifier):
        _parse_identifier([])


@pytest.mark.parametrize(('tokens', 'expected_value', 'expected_count'), [
    ([Token(Token.IDENTIFIER, 'ident')],
     Identifier('ident'),
     1),
    ([Token(Token.NUMBER, '1')],
     Number('1'),
     1),
    ([Token(Token.IDENTIFIER, 'x'), Token(Token.IDENTIFIER, 't')],
     Identifier('x', alias='t'),
     2),
    ([Token(Token.IDENTIFIER, 'x'),
      Token(Token.AS, 'as'),
      Token(Token.IDENTIFIER, 't')],
     Identifier('x', as_='as', alias='t'),
     3),
])
def test_parse_identifier(tokens, expected_value, expected_count):
    result, count = _parse_identifier(tokens)

    assert count == expected_count
    assert result == expected_value


def test_parse_from_1(from_1):
    assert_statements(from_1.tokens, from_1.statements)


def test_parse_from_2(from_2):
    assert_statements(from_2.tokens, from_2.statements)


def test_parse_from_3(from_3):
    assert_statements(from_3.tokens, from_3.statements)


def test_parse_from_4(from_4):
    assert_statements(from_4.tokens, from_4.statements)


def test_parse_from_5(from_5):
    assert_statements(from_5.tokens, from_5.statements)


def test_parse_func_1(func_1):
    assert_statements(func_1.tokens, func_1.statements)


def test_parse_func_2(func_2):
    assert_statements(func_2.tokens, func_2.statements)


def test_parse_func_3(func_3):
    assert_statements(func_3.tokens, func_3.statements)


def test_parse_func_4(func_4):
    assert_statements(func_4.tokens, func_4.statements)


def test_parse_group_by_1(group_by_1):
    assert_statements(group_by_1.tokens, group_by_1.statements)


def test_parse_group_by_2(group_by_2):
    assert_statements(group_by_2.tokens, group_by_2.statements)


def test_parse_group_by_3(group_by_3):
    assert_statements(group_by_3.tokens, group_by_3.statements)


def test_parse_group_by_4(group_by_4):
    assert_statements(group_by_4.tokens, group_by_4.statements)


def test_parse_having_1(having_1):
    assert_statements(having_1.tokens, having_1.statements)


def test_parse_having_2(having_2):
    assert_statements(having_2.tokens, having_2.statements)


def test_parse_limit_1(limit_1):
    assert_statements(limit_1.tokens, limit_1.statements)


def test_parse_limit_2(limit_2):
    assert_statements(limit_2.tokens, limit_2.statements)


def test_parse_limit_3(limit_3):
    assert_statements(limit_3.tokens, limit_3.statements)


def test_parse_order_by_1(order_by_1):
    assert_statements(order_by_1.tokens, order_by_1.statements)


def test_parse_order_by_2(order_by_2):
    assert_statements(order_by_2.tokens, order_by_2.statements)


def test_parse_order_by_3(order_by_3):
    assert_statements(order_by_3.tokens, order_by_3.statements)


def test_parse_order_by_4(order_by_4):
    assert_statements(order_by_4.tokens, order_by_4.statements)


def test_parse_select_1(select_1):
    assert_statements(select_1.tokens, select_1.statements)


def test_parse_select_2(select_2):
    assert_statements(select_2.tokens, select_2.statements)


def test_parse_select_3(select_3):
    assert_statements(select_3.tokens, select_3.statements)


def test_parse_select_4(select_4):
    assert_statements(select_4.tokens, select_4.statements)


def test_parse_where_1(where_1):
    assert_statements(where_1.tokens, where_1.statements)


def test_parse_where_2(where_2):
    assert_statements(where_2.tokens, where_2.statements)


def test_parse_where_3(where_3):
    assert_statements(where_3.tokens, where_3.statements)


def test_parse_where_4(where_4):
    assert_statements(where_4.tokens, where_4.statements)


def test_parse_where_5(where_5):
    assert_statements(where_5.tokens, where_5.statements)


def test_parse_where_6(where_6):
    assert_statements(where_6.tokens, where_6.statements)


def test_parse_where_7(where_7):
    assert_statements(where_7.tokens, where_7.statements)


def test_parse_where_8(where_8):
    assert_statements(where_8.tokens, where_8.statements)


def test_parse_where_9(where_9):
    assert_statements(where_9.tokens, where_9.statements)


def test_parse_where_10(where_10):
    assert_statements(where_10.tokens, where_10.statements)


def test_parse_composition_1(composition_1):
    assert_statements(composition_1.tokens, composition_1.statements)


def test_parse_composition_2(composition_2):
    assert_statements(composition_2.tokens, composition_2.statements)


def test_parse_multiple_statements_1(multiple_statements_1):
    assert_statements(multiple_statements_1.tokens,
                      multiple_statements_1.statements)
