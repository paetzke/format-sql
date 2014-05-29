# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from format_sql.styler import style


def _test(data):
    expected = '\n'.join(data.style)
    assert expected == style(data.statements)


def test_style_select_with_filter_in_list(select_with_filter_in_list):
    _test(select_with_filter_in_list)


def test_style_select_with_limit(select_with_limit):
    _test(select_with_limit)


def test_style_select_with_multiple_columns(select_with_multiple_columns):
    _test(select_with_multiple_columns)


def test_style_select_from(select_from):
    _test(select_from)


def test_style_select_with_group_and_having(select_with_group_and_having):
    _test(select_with_group_and_having)


def test_style_select_with_join(select_with_join):
    _test(select_with_join)


def test_style_join_with_nested_on(join_with_nested_on):
    _test(join_with_nested_on)


def test_stlye_select_with_join_and_nested_filters(select_with_join_and_nested_filters):
    _test(select_with_join_and_nested_filters)


def test_style_select_with_where(select_with_where):
    _test(select_with_where)


def test_style_select_with_join_and_on(select_with_join_and_on):
    _test(select_with_join_and_on)


def test_style_select_with_where_filters(select_with_where_filters):
    _test(select_with_where_filters)


def test_style_select_with_join_with_and(select_with_join_with_and):
    _test(select_with_join_with_and)


def test_style_select_with_limit_and_offset(select_with_limit_and_offset):
    _test(select_with_limit_and_offset)


def test_style_select_with_complex_filter(select_with_complex_filter):
    _test(select_with_complex_filter)


def test_style_select_with_sub_select_in_filter(select_with_sub_select_in_filter):
    _test(select_with_sub_select_in_filter)


def test_style_select_with_complex_having(select_with_complex_having):
    _test(select_with_complex_having)


def test_style_select_with_not_in_compare(select_with_not_in_compare):
    _test(select_with_not_in_compare)


def test_style_select_with_multiple_joins(select_with_multiple_joins):
    _test(select_with_multiple_joins)


def test_style_select_in_from(select_in_from):
    _test(select_in_from)


def test_style_select_in_from_and_join(select_in_from_and_join):
    _test(select_in_from_and_join)
