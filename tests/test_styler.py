# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014-2015, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from __future__ import unicode_literals

from format_sql.styler import Liner, _style_func, style


def assert_func_style(statements1, styled2):
    liner = Liner()
    _style_func(statements1[0], liner)
    assert styled2 == liner.lines


def assert_style(statements1, styled2):
    assert style(statements1) == styled2


def test_from_1(from_1):
    assert_style(from_1.statements, from_1.style)


def test_from_2(from_2):
    assert_style(from_2.statements, from_2.style)


def test_from_3(from_3):
    assert_style(from_3.statements, from_3.style)


def test_from_4(from_4):
    assert_style(from_4.statements, from_4.style)


def test_from_5(from_5):
    assert_style(from_5.statements, from_5.style)


def test_from_6(from_6):
    assert_style(from_6.statements, from_6.style)


def test_func_1(func_1):
    assert_func_style(func_1.statements, func_1.style)


def test_func_2(func_2):
    assert_func_style(func_2.statements, func_2.style)


def test_func_3(func_3):
    assert_func_style(func_3.statements, func_3.style)


def test_func_4(func_4):
    assert_func_style(func_4.statements, func_4.style)


def test_group_by_1(group_by_1):
    assert_style(group_by_1.statements, group_by_1.style)


def test_group_by_2(group_by_2):
    assert_style(group_by_2.statements, group_by_2.style)


def test_group_by_3(group_by_3):
    assert_style(group_by_3.statements, group_by_3.style)


def test_group_by_4(group_by_4):
    assert_style(group_by_4.statements, group_by_4.style)


def test_having_1(having_1):
    assert_style(having_1.statements, having_1.style)


def test_having_2(having_2):
    assert_style(having_2.statements, having_2.style)


def test_limit_1(limit_1):
    assert_style(limit_1.statements, limit_1.style)


def test_limit_2(limit_2):
    assert_style(limit_2.statements, limit_2.style)


def test_limit_3(limit_3):
    assert_style(limit_3.statements, limit_3.style)


def test_order_by_1(order_by_1):
    assert_style(order_by_1.statements, order_by_1.style)


def test_order_by_2(order_by_2):
    assert_style(order_by_2.statements, order_by_2.style)


def test_order_by_3(order_by_3):
    assert_style(order_by_3.statements, order_by_3.style)


def test_order_by_4(order_by_4):
    assert_style(order_by_4.statements, order_by_4.style)


def test_select_1(select_1):
    assert_style(select_1.statements, select_1.style)


def test_select_2(select_2):
    assert_style(select_2.statements, select_2.style)


def test_select_3(select_3):
    assert_style(select_3.statements, select_3.style)


def test_where_1(where_1):
    assert_style(where_1.statements, where_1.style)


def test_where_2(where_2):
    assert_style(where_2.statements, where_2.style)


def test_where_3(where_3):
    assert_style(where_3.statements, where_3.style)


def test_where_4(where_4):
    assert_style(where_4.statements, where_4.style)


def test_where_5(where_5):
    assert_style(where_5.statements, where_5.style)


def test_where_6(where_6):
    assert_style(where_6.statements, where_6.style)


def test_where_7(where_7):
    assert_style(where_7.statements, where_7.style)


def test_where_8(where_8):
    assert_style(where_8.statements, where_8.style)


def test_where_9(where_9):
    assert_style(where_9.statements, where_9.style)


def test_where_10(where_10):
    assert_style(where_10.statements, where_10.style)


def test_composition_1(composition_1):
    assert_style(composition_1.statements, composition_1.style)


def test_composition_2(composition_2):
    assert_style(composition_2.statements, composition_2.style)


def test_multiple_statements_1(multiple_statements_1):
    assert_style(multiple_statements_1.statements, multiple_statements_1.style)
