# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (f.paetzke@gmail.com)
All rights reserved.

"""
from format_sql import format_sql


def assert_format(sql, expected):
    result = format_sql(sql)
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


def test_08():
    sql = "SELECT x1,x2 AS t,x3,count(1) FROM my_table AS t1 LEFT JOIN my_table2 WHERE t=3 OR x in ('78','d');"
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


def test_09():
    sql = 'SELECT * FROM my_table AS t1 LEFT JOIN my_table2 WHERE t =3;'
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


def test_10():
    sql = 'SELECT * FROM my_table AS t1 LEFT JOIN my_table2 WHERE t =3'
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    my_table AS t1',
        '    LEFT JOIN my_table2',
        'WHERE',
        '    t = 3',
    ])

    assert_format(sql, expected)


def test_11():
    sql = 'SELECT name, some_par1  FROM  zauber_table WHERE  some_par1 IN (SELECT some_par1 FROM some_special_table)'
    expected = '\n'.join([
        'SELECT',
        '    name,',
        '    some_par1',
        'FROM',
        '    zauber_table',
        'WHERE',
        '    some_par1 IN (',
        '        SELECT',
        '            some_par1',
        '        FROM',
        '            some_special_table)',
    ])

    assert_format(sql, expected)


def test_12():
    sql = 'SELECT geodaten_id FROM geodaten WHERE geodaten_id IN (SELECT id FROM id_check);'
    expected = '\n'.join([
        'SELECT',
        '    geodaten_id',
        'FROM',
        '    geodaten',
        'WHERE',
        '    geodaten_id IN (',
        '        SELECT',
        '            id',
        '        FROM',
        '            id_check);',
    ])

    assert_format(sql, expected)


def test_13():
    sql = 'SELECT name, some_par1  FROM  zauber_table WHERE  some_par1 < ALL (SELECT some_par1 FROM some_special_table)'
    expected = '\n'.join([
        'SELECT',
        '    name,',
        '    some_par1',
        'FROM',
        '    zauber_table',
        'WHERE',
        '    some_par1 < ALL (',
        '        SELECT',
        '            some_par1',
        '        FROM',
        '            some_special_table)',
    ])

    assert_format(sql, expected)


def test_14():
    sql = 'SELECT name, some_par1  FROM  zauber_table WHERE  some_par1 < ALL (select some_par1 FROM some_special_table )'
    expected = '\n'.join([
        'SELECT',
        '    name,',
        '    some_par1',
        'FROM',
        '    zauber_table',
        'WHERE',
        '    some_par1 < ALL (',
        '        SELECT',
        '            some_par1',
        '        FROM',
        '            some_special_table)',
    ])

    assert_format(sql, expected)


def test_15():
    sql = 'SELECT name, some_par1 FROM zauber_table WHERE some_par1 < ALL ( select some_par1 FROM some_special_table)'
    expected = '\n'.join([
        'SELECT',
        '    name,',
        '    some_par1',
        'FROM',
        '    zauber_table',
        'WHERE',
        '    some_par1 < ALL (',
        '        SELECT',
        '            some_par1',
        '        FROM',
        '            some_special_table)',
    ])

    assert_format(sql, expected)
