# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (f.paetzke@gmail.com)
All rights reserved.

"""
from format_sql import pretty_format


def assert_format(sql, expected):
    result = pretty_format(sql)
    assert result == expected


def test_00():
    sql = 'SELECT * FROM my_table;'
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    my_table;'
    ])

    assert_format(sql, expected)


def test_01():
    sql = 'SELECT * FROM my_table AS t1 LEFT JOIN my_table2;'
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    my_table AS t1',
        '    LEFT JOIN my_table2;',
    ])

    assert_format(sql, expected)


def test_02():
    sql = 'SELECT * FROM my_table AS t1 LEFT JOIN my_table2 WHERE t = 3;'
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    my_table AS t1',
        '    LEFT JOIN my_table2',
        'WHERE',
        '    t = 3;',
    ])

    assert_format(sql, expected)


def test_03():
    sql = "SELECT * FROM my_table AS t1 LEFT JOIN my_table2 WHERE t = 3 AND x = '78';"
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    my_table AS t1',
        '    LEFT JOIN my_table2',
        'WHERE',
        '    t = 3',
        "    AND x = '78';",
    ])

    assert_format(sql, expected)


def test_04():
    sql = "SELECT * FROM my_table AS t1 LEFT JOIN my_table2 WHERE t = 3 OR x = '78';"
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    my_table AS t1',
        '    LEFT JOIN my_table2',
        'WHERE',
        '    t = 3',
        "    OR x = '78';",
    ])

    assert_format(sql, expected)


def test_05():
    sql = "SELECT * FROM my_table AS t1 LEFT JOIN my_table2 WHERE t = 3 OR x in ('78', 'd');"
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    my_table AS t1',
        '    LEFT JOIN my_table2',
        'WHERE',
        '    t = 3',
        "    OR x IN ('78', 'd');",
    ])

    assert_format(sql, expected)


def test_06():
    sql = "SELECT x1,x2,x3 FROM my_table AS t1 LEFT JOIN my_table2 WHERE t = 3 OR x in ('78', 'd');"
    expected = '\n'.join([
        'SELECT',
        '    x1,',
        '    x2,',
        '    x3',
        'FROM',
        '    my_table AS t1',
        '    LEFT JOIN my_table2',
        'WHERE',
        '    t = 3',
        "    OR x IN ('78', 'd');",
    ])

    assert_format(sql, expected)


def test_07():
    sql = "SELECT x1,x2 AS t,x3,count(1) FROM my_table AS t1 LEFT JOIN my_table2 WHERE t = 3 OR x in ('78', 'd');"
    expected = '\n'.join([
        'SELECT',
        '    x1,',
        '    x2 AS t,',
        '    x3,',
        '    count(1)',
        'FROM',
        '    my_table AS t1',
        '    LEFT JOIN my_table2',
        'WHERE',
        '    t = 3',
        "    OR x IN ('78', 'd');",
    ])

    assert_format(sql, expected)
