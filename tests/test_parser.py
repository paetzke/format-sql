# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from format_sql.parser import parse
from format_sql.tokenizer import Token, Type


def assert_statement(statements1, statements2):
    assert len(statements1) == len(statements2)
    for statement1, statement2 in zip(statements1, statements2):
        assert statement1.value == statement2.value
        assert type(statement1) == type(statement2)
        assert_statement(statement1.statements, statement2.statements)


def _test(data):
    result = parse(data.tokens)
    assert_statement(data.statements, result)


def test_parse_select_with_filter_in_list(select_with_filter_in_list):
    _test(select_with_filter_in_list)


def test_parse_select_with_limit(select_with_limit):
    _test(select_with_limit)


def test_parse_select_from(select_from):
    _test(select_from)


def test_parse_select_with_multiple_columns(select_with_multiple_columns):
    _test(select_with_multiple_columns)


def test_parse_select_with_limit_and_offset(select_with_limit_and_offset):
    _test(select_with_limit_and_offset)


def test_parse_select_with_group_and_having(select_with_group_and_having):
    _test(select_with_group_and_having)


def test_parse_select_with_join(select_with_join):
    _test(select_with_join)


def test_parse_join_with_nested_on(join_with_nested_on):
    _test(join_with_nested_on)


def test_parse_select_with_where(select_with_where):
    _test(select_with_where)


def test_parse_select_with_join_and_on(select_with_join_and_on):
    _test(select_with_join_and_on)


def test_parse_select_with_where_filters(select_with_where_filters):
    _test(select_with_where_filters)


def test_parse_select_with_join_with_and(select_with_join_with_and):
    _test(select_with_join_with_and)


def test_parse_select_with_complex_filter(select_with_complex_filter):
    _test(select_with_complex_filter)


def test_parse_select_with_sub_select_in_filter(select_with_sub_select_in_filter):
    _test(select_with_sub_select_in_filter)


def test_parse_select_with_complex_having(select_with_complex_having):
    _test(select_with_complex_having)


def test_parse_select_with_not_in_compare(select_with_not_in_compare):
    _test(select_with_not_in_compare)


def test_parse_select_with_multiple_joins(select_with_multiple_joins):
    _test(select_with_multiple_joins)


def test_parse_select_in_from(select_in_from):
    _test(select_in_from)


def test_parse_select_in_from_and_join(select_in_from_and_join):
    _test(select_in_from_and_join)


def test_parse_select_with_single_order_value(select_with_single_order_value):
    _test(select_with_single_order_value)


def test_parse_select_with_order_values(select_with_order_values):
    _test(select_with_order_values)


def test_parse_can_handle_unknown_combinations():
    """
    Here we assert that the function returns at all in a short time. Maybe
    there is a better way to do that.

    """
    tokens = [
        Token(Type.SELECT,  'SELECT'),
        Token(Type.STR, '*'),
        Token(Type.FROM, 'FROM'),
        Token(Type.STR, 'MY_TABLE'),
        Token(Type.COMPARE, '<'),
        Token(Type.STR, 'xyz'),
        Token(Type.COMPARE, '>'),
        Token(Type.STR, ';')
    ]

    parse(tokens)
