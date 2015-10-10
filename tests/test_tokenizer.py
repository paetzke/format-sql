# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014-2015, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
import pytest
from format_sql.tokenizer import StringNotTerminated, Token, tokenize

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest


def assert_tokens(tokens1, tokens2):
    tokens2 = list(tokens2)
    for tk1, tk2 in zip_longest(tokens1, tokens2):
        assert tk1._value == tk2._value, ">%s< >%s<" % (tk1, tk2)
        assert tk1._type == tk2._type, ">%s< >%s<" % (tk1, tk2)


@pytest.mark.parametrize(('sql', 'expected_tokens'), [
    ('GROUP BY year', [
        (Token.GROUP_BY, 'GROUP BY'),
        (Token.IDENTIFIER, 'year'),
    ]),
    ('GROUP BY year, country, product', [
        (Token.GROUP_BY, 'GROUP BY'),
        (Token.IDENTIFIER, 'year'),
        (Token.COMMA, ','),
        (Token.IDENTIFIER, 'country'),
        (Token.COMMA, ','),
        (Token.IDENTIFIER, 'product'),
    ]),
    ('GROUP BY year, country, product With Rollup',  [
        (Token.GROUP_BY, 'GROUP BY'),
        (Token.IDENTIFIER, 'year'),
        (Token.COMMA, ','),
        (Token.IDENTIFIER, 'country'),
        (Token.COMMA, ','),
        (Token.IDENTIFIER, 'product'),
        (Token.WITH_ROLLUP, 'With Rollup'),
    ]),
    ('select count(1) from my_table', [
        (Token.SELECT, 'select'),
        (Token.FUNC, 'count'),
        (Token.PARENTHESIS_OPEN, '('),
        (Token.NUMBER, '1'),
        (Token.PARENTHESIS_CLOSE, ')'),
        (Token.FROM, 'from'),
        (Token.IDENTIFIER, 'my_table'),
    ]),
    ('select distinct count(1) from my_table', [
        (Token.SELECT, 'select distinct'),
        (Token.FUNC, 'count'),
        (Token.PARENTHESIS_OPEN, '('),
        (Token.NUMBER, '1'),
        (Token.PARENTHESIS_CLOSE, ')'),
        (Token.FROM, 'from'),
        (Token.IDENTIFIER, 'my_table'),
    ]),
    ('GROUP   by year, country, product With Rollup',  [
        (Token.GROUP_BY, 'GROUP   by'),
        (Token.IDENTIFIER, 'year'),
        (Token.COMMA, ','),
        (Token.IDENTIFIER, 'country'),
        (Token.COMMA, ','),
        (Token.IDENTIFIER, 'product'),
        (Token.WITH_ROLLUP, 'With Rollup'),
    ]),
    ('select  count\n(distinct(1)) from my_table', [
        (Token.SELECT, 'select'),
        (Token.FUNC, 'count'),
        (Token.PARENTHESIS_OPEN, '('),
        (Token.FUNC, 'distinct'),
        (Token.PARENTHESIS_OPEN, '('),
        (Token.NUMBER, '1'),
        (Token.PARENTHESIS_CLOSE, ')'),
        (Token.PARENTHESIS_CLOSE, ')'),
        (Token.FROM, 'from'),
        (Token.IDENTIFIER, 'my_table'),
    ]),
    ('select count(1) as cnt from my_table', [
        (Token.SELECT, 'select'),
        (Token.FUNC, 'count'),
        (Token.PARENTHESIS_OPEN, '('),
        (Token.NUMBER, '1'),
        (Token.PARENTHESIS_CLOSE, ')'),
        (Token.AS, 'as'),
        (Token.IDENTIFIER, 'cnt'),
        (Token.FROM, 'from'),
        (Token.IDENTIFIER, 'my_table'),
    ]),

])
def test_tokenize(sql, expected_tokens):
    tokens = [Token(token_type, token_value)
              for token_type, token_value in expected_tokens]

    assert_tokens(tokens, tokenize(sql))


@pytest.mark.parametrize(('sql', 'expected_token'), [
    ('123', (Token.NUMBER, '123')),
    ('1.23', (Token.NUMBER, '1.23')),
    ('-1.23', (Token.NUMBER, '-1.23')),
    ('+1.23', (Token.NUMBER, '+1.23')),
])
def test_tokenize_numbers(sql, expected_token):
    token_type, token_value = expected_token
    token = Token(token_type, token_value)

    assert_tokens([token], tokenize(sql))


@pytest.mark.parametrize(('sql', 'expected_token'), [
    ('"s s( ) ss"', (Token.STR, '"s s( ) ss"')),
    ("'s s( ) ss'", (Token.STR, "'s s( ) ss'")),
])
def test_tokenize_strs(sql, expected_token):
    token_type, token_value = expected_token
    token = Token(token_type, token_value)

    assert_tokens([token], tokenize(sql))


@pytest.mark.parametrize(('sql', 'expected_token'), [
    ('xyz', (Token.IDENTIFIER, 'xyz')),
    ('xy1', (Token.IDENTIFIER, 'xy1')),
    ('xy1.tf', (Token.IDENTIFIER, 'xy1.tf')),
    ('*', (Token.IDENTIFIER, '*')),
    ('t.*', (Token.IDENTIFIER, 't.*')),
    ('%(t)s', (Token.IDENTIFIER, '%(t)s')),
    ('%(t_s)s', (Token.IDENTIFIER, '%(t_s)s')),
    ('`xy1`.`tf`', (Token.IDENTIFIER, '`xy1`.`tf`')),
    ('`xy1``', (Token.IDENTIFIER, '`xy1`')),
    ('%s', (Token.IDENTIFIER, '%s')),
])
def test_tokenize_identifier(sql, expected_token):
    token_type, token_value = expected_token
    token = Token(token_type, token_value)

    assert_tokens([token], tokenize(sql))


@pytest.mark.parametrize(('sql', 'expected_token'), [
    ('Join', (Token.JOIN, 'Join')),
    ('Inner Join', (Token.JOIN, 'Inner Join')),
    ('natural Join', (Token.JOIN, 'natural Join')),
    ('LEFT  Join', (Token.JOIN, 'LEFT  Join')),
    ('LEFT  OUTER Join', (Token.JOIN, 'LEFT  OUTER Join')),
    ('Right  Join', (Token.JOIN, 'Right  Join')),
    ('Right  OUTER Join', (Token.JOIN, 'Right  OUTER Join')),
])
def test_tokenize_join(sql, expected_token):
    token_type, token_value = expected_token
    token = Token(token_type, token_value)

    assert_tokens([token], tokenize(sql))


@pytest.mark.parametrize(('sql', 'expected_token'), [
    ('Select', (Token.SELECT, 'Select')),
    ('Select distinct', (Token.SELECT, 'Select distinct')),
    ('Select sql_no_cache', (Token.SELECT, 'Select sql_no_cache')),
    ('SELECT SQL_CALC_FOUND_ROWS',
     (Token.SELECT, 'SELECT SQL_CALC_FOUND_ROWS')),
])
def test_tokenize_select(sql, expected_token):
    token_type, token_value = expected_token
    token = Token(token_type, token_value)

    assert_tokens([token], tokenize(sql))


@pytest.mark.parametrize(('sql', 'expected_token'), [
    ('=', (Token.COMPARE, '=')),
    ('<>', (Token.COMPARE, '<>')),
    ('<', (Token.COMPARE, '<')),
    ('>', (Token.COMPARE, '>')),
    ('!=', (Token.COMPARE, '!=')),
    ('>=', (Token.COMPARE, '>=')),
    ('<=', (Token.COMPARE, '<=')),
])
def test_tokenize_compare(sql, expected_token):
    token_type, token_value = expected_token
    token = Token(token_type, token_value)

    assert_tokens([token], tokenize(sql))


@pytest.mark.parametrize(('sql', 'expected_token'), [
    ('and', (Token.LINK, 'and')),
    ('Or', (Token.LINK, 'Or')),
])
def test_tokenize_link(sql, expected_token):
    token_type, token_value = expected_token
    token = Token(token_type, token_value)

    assert_tokens([token], tokenize(sql))


@pytest.mark.parametrize('sql', [
    '"213',
    '"s s( ) ss\'',
])
def test_tokenize_str_is_not_terminated(sql):
    with pytest.raises(StringNotTerminated):
        list(tokenize(sql))


def test_tokenize_from_1(from_1):
    assert_tokens(from_1.tokens, tokenize(from_1.sql))


def test_tokenize_from_2(from_2):
    assert_tokens(from_2.tokens, tokenize(from_2.sql))


def test_tokenize_from_3(from_3):
    assert_tokens(from_3.tokens, tokenize(from_3.sql))


def test_tokenize_from_4(from_4):
    assert_tokens(from_4.tokens, tokenize(from_4.sql))


def test_tokenize_from_5(from_5):
    assert_tokens(from_5.tokens, tokenize(from_5.sql))


def test_tokenize_from_6(from_6):
    assert_tokens(from_6.tokens, tokenize(from_6.sql))


def test_tokenize_from_7(from_7):
    assert_tokens(from_7.tokens, tokenize(from_7.sql))


def test_tokenize_from_8(from_8):
    assert_tokens(from_8.tokens, tokenize(from_8.sql))


def test_tokenize_from_9(from_9):
    assert_tokens(from_9.tokens, tokenize(from_9.sql))


def test_tokenize_func_1(func_1):
    assert_tokens(func_1.tokens, tokenize(func_1.sql))


def test_tokenize_func_2(func_2):
    assert_tokens(func_2.tokens, tokenize(func_2.sql))


def test_tokenize_func_3(func_3):
    assert_tokens(func_3.tokens, tokenize(func_3.sql))


def test_tokenize_func_4(func_4):
    assert_tokens(func_4.tokens, tokenize(func_4.sql))


def test_tokenize_func_5(func_5):
    assert_tokens(func_5.tokens, tokenize(func_5.sql))


def test_tokenize_group_by_1(group_by_1):
    assert_tokens(group_by_1.tokens, tokenize(group_by_1.sql))


def test_tokenize_group_by_2(group_by_2):
    assert_tokens(group_by_2.tokens, tokenize(group_by_2.sql))


def test_tokenize_group_by_3(group_by_3):
    assert_tokens(group_by_3.tokens, tokenize(group_by_3.sql))


def test_tokenize_group_by_4(group_by_4):
    assert_tokens(group_by_4.tokens, tokenize(group_by_4.sql))


def test_tokenize_having_1(having_1):
    assert_tokens(having_1.tokens, tokenize(having_1.sql))


def test_tokenize_having_2(having_2):
    assert_tokens(having_2.tokens, tokenize(having_2.sql))


def test_tokenize_limit_1(limit_1):
    assert_tokens(limit_1.tokens, tokenize(limit_1.sql))


def test_tokenize_limit_2(limit_2):
    assert_tokens(limit_2.tokens, tokenize(limit_2.sql))


def test_tokenize_limit_3(limit_3):
    assert_tokens(limit_3.tokens, tokenize(limit_3.sql))


def test_tokenize_order_by_1(order_by_1):
    assert_tokens(order_by_1.tokens, tokenize(order_by_1.sql))


def test_tokenize_order_by_2(order_by_2):
    assert_tokens(order_by_2.tokens, tokenize(order_by_2.sql))


def test_tokenize_order_by_3(order_by_3):
    assert_tokens(order_by_3.tokens, tokenize(order_by_3.sql))


def test_tokenize_order_by_4(order_by_4):
    assert_tokens(order_by_4.tokens, tokenize(order_by_4.sql))


def test_tokenize_select_1(select_1):
    assert_tokens(select_1.tokens, tokenize(select_1.sql))


def test_tokenize_select_2(select_2):
    assert_tokens(select_2.tokens, tokenize(select_2.sql))


def test_tokenize_select_3(select_3):
    assert_tokens(select_3.tokens, tokenize(select_3.sql))


def test_tokenize_select_4(select_4):
    assert_tokens(select_4.tokens, tokenize(select_4.sql))


def test_tokenize_where_1(where_1):
    assert_tokens(where_1.tokens, tokenize(where_1.sql))


def test_tokenize_where_2(where_2):
    assert_tokens(where_2.tokens, tokenize(where_2.sql))


def test_tokenize_where_3(where_3):
    assert_tokens(where_3.tokens, tokenize(where_3.sql))


def test_tokenize_where_4(where_4):
    assert_tokens(where_4.tokens, tokenize(where_4.sql))


def test_tokenize_where_5(where_5):
    assert_tokens(where_5.tokens, tokenize(where_5.sql))


def test_tokenize_where_6(where_6):
    assert_tokens(where_6.tokens, tokenize(where_6.sql))


def test_tokenize_where_7(where_7):
    assert_tokens(where_7.tokens, tokenize(where_7.sql))


def test_tokenize_where_8(where_8):
    assert_tokens(where_8.tokens, tokenize(where_8.sql))


def test_tokenize_where_9(where_9):
    assert_tokens(where_9.tokens, tokenize(where_9.sql))


def test_tokenize_where_10(where_10):
    assert_tokens(where_10.tokens, tokenize(where_10.sql))


def test_tokenize_where_11(where_11):
    assert_tokens(where_11.tokens, tokenize(where_11.sql))


def test_tokenize_where_12(where_12):
    assert_tokens(where_12.tokens, tokenize(where_12.sql))


def test_tokenize_composition_1(composition_1):
    assert_tokens(composition_1.tokens, tokenize(composition_1.sql))


def test_tokenize_composition_2(composition_2):
    assert_tokens(composition_2.tokens, tokenize(composition_2.sql))


def test_tokenize_composition_3(composition_3):
    assert_tokens(composition_3.tokens, tokenize(composition_3.sql))


def test_tokenize_multiple_statements1(multiple_statements_1):
    assert_tokens(multiple_statements_1.tokens,
                  tokenize(multiple_statements_1.sql))


def test_tokenize_insert1(insert_1):
    assert_tokens(insert_1.tokens, tokenize(insert_1.sql))


def test_tokenize_insert2(insert_2):
    assert_tokens(insert_2.tokens, tokenize(insert_2.sql))


def test_tokenize_insert3(insert_3):
    assert_tokens(insert_3.tokens, tokenize(insert_3.sql))


def test_tokenize_insert4(insert_4):
    assert_tokens(insert_4.tokens, tokenize(insert_4.sql))


def test_tokenize_between_1(between_1):
    assert_tokens(between_1.tokens, tokenize(between_1.sql))


def test_tokenize_like_1(like_1):
    assert_tokens(like_1.tokens, tokenize(like_1.sql))
