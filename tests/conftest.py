# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from collections import namedtuple

from format_sql.parser import (Comma, Compare, From, Group, Having, Identifier,
                               Join, Key, Limit, Link, Select, Sub, Where)
from format_sql.tokenizer import Token, Type
from pytest import fixture

Data = namedtuple('Data', ['sql', 'tokens', 'statements', 'style'])


@fixture
def select_with_limit():
    return Data(
        sql='SELECT * FROM my_table LIMIT 65',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'my_table'),
            Token(Type.LIMIT, 'LIMIT'),
            Token(Type.STR, '65'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[Identifier('my_table')]),
            Limit('LIMIT', statements=[Identifier('65')]),
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    my_table',
            'LIMIT',
            '    65',
            ''
        ])


@fixture
def select_with_limit_and_offset():
    return Data(
        sql='SELECT * FROM my_table LIMIT 65,90',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'my_table'),
            Token(Type.LIMIT, 'LIMIT'),
            Token(Type.STR, '65'),
            Token(Type.PUNCTUATION, ','),
            Token(Type.STR, '90'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[Identifier('my_table')]),
            Limit('LIMIT', statements=[
                Identifier('65'),
                Comma(','),
                Identifier('90')])
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    my_table',
            'LIMIT',
            '    65,',
            '    90',
            ''
        ])


@fixture
def select_from():
    return Data(
        sql='SELECT * FROM my_table',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'my_table'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[Identifier('my_table')]),
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    my_table',
            ''
        ])


@fixture
def select_with_multiple_columns():
    return Data(
        sql='SELECT a, b, c',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, 'a'),
            Token(Type.PUNCTUATION, ','),
            Token(Type.STR, 'b'),
            Token(Type.PUNCTUATION, ','),
            Token(Type.STR, 'c'),
        ],
        statements=[
            Select('SELECT', statements=[
                Identifier('a'),
                Comma(','),
                Identifier('b'),
                Comma(','),
                Identifier('c'),
            ])
        ],
        style=[
            'SELECT',
            '    a,',
            '    b,',
            '    c',
            ''
        ])


@fixture
def select_with_where():
    return Data(
        sql='',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'my_table2'),
            Token(Type.WHERE, 'WHERE'),
            Token(Type.STR, 't'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, '3'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[Identifier('my_table2')]),
            Where('WHERE', statements=[Compare('t = 3')]),
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    my_table2',
            'WHERE',
            '    t = 3',
            ''
        ])


@fixture
def select_with_where_filters():
    return Data(
        sql='SELECT * FROM tab1 WHERE id1 = value1 OR id2 = value2',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'tab1'),
            Token(Type.WHERE, 'WHERE'),
            Token(Type.STR, 'id1'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'value1'),
            Token(Type.LINK, 'OR'),
            Token(Type.STR, 'id2'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'value2'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[Identifier('tab1')]),
            Where('WHERE', statements=[
                Compare('id1 = value1'),
                Link('OR'),
                Compare('id2 = value2'),
            ]),
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    tab1',
            'WHERE',
            '    id1 = value1',
            '    OR id2 = value2',
            ''
        ])


@fixture
def select_with_join():
    return Data(
        sql='SELECT * FROM tab1 RIGHT JOIN tab2',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'tab1'),
            Token(Type.JOIN, 'RIGHT JOIN'),
            Token(Type.STR, 'tab2'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[
                Identifier('tab1'),
                Join('RIGHT JOIN'),
                Identifier('tab2'),
            ]),
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    tab1',
            '    RIGHT JOIN tab2',
            ''
        ])


@fixture
def select_with_join_and_on():
    return Data(
        sql='SELECT * FROM tab1 INNER JOIN tab2 ON tab1.id = tab2.id',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'tab1'),
            Token(Type.JOIN, 'INNER JOIN'),
            Token(Type.STR, 'tab2'),
            Token(Type.KEYWORD, 'ON'),
            Token(Type.STR, 'tab1.id'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'tab2.id'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[
                Identifier('tab1'),
                Join('INNER JOIN'),
                Identifier('tab2'),
                Key('ON'),
                Compare('tab1.id = tab2.id'),
            ]),
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    tab1',
            '    INNER JOIN tab2',
            '        ON tab1.id = tab2.id',
            ''
        ])


@fixture
def select_with_join_and_nested_filters():
    return Data(
        sql='',
        tokens='',
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[Identifier('tab1')]),
            Where('WHERE', statements=[
                Compare('id1 = value1'),
                Link('AND'),
                Sub('(', statements=[
                    Compare('tab1.id = tab2.id'),
                    Link('OR'),
                    Compare('tab1.id2 = tab2.id2'),
                ])
            ]),
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    tab1',
            'WHERE',
            '    id1 = value1',
            '    AND (',
            '        tab1.id = tab2.id',
            '        OR tab1.id2 = tab2.id2)',
            ''
        ])


@fixture
def join_with_nested_on():
    return Data(
        sql='',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'tab1'),
            Token(Type.JOIN, 'INNER JOIN'),
            Token(Type.STR, 'tab2'),
            Token(Type.KEYWORD, 'ON'),
            Token(Type.PUNCTUATION, '('),
            Token(Type.STR, 'tab1.id'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'tab2.id'),
            Token(Type.LINK, 'AND'),
            Token(Type.STR, 'tab1.id2'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'tab2.id2'),
            Token(Type.PUNCTUATION, ')'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[
                Identifier('tab1'),
                Join('INNER JOIN'),
                Identifier('tab2'),
                Key('ON'),
                Sub('(', statements=[
                    Compare('tab1.id = tab2.id'),
                    Link('AND'),
                    Compare('tab1.id2 = tab2.id2'),
                ])
            ]),
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    tab1',
            '    INNER JOIN tab2',
            '        ON (',
            '            tab1.id = tab2.id',
            '            AND tab1.id2 = tab2.id2)',
            ''
        ])


@fixture
def select_with_filter_in_list():
    return Data(
        sql='SELECT x3 FROM tab1 WHERE x IN ("78", "d")',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, 'x3'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'tab1'),
            Token(Type.WHERE, 'WHERE'),
            Token(Type.STR, 'x'),
            Token(Type.COMPARE, 'IN'),
            Token(Type.PUNCTUATION, '('),
            Token(Type.STR, '"78"'),
            Token(Type.PUNCTUATION, ','),
            Token(Type.STR, '"d"'),
            Token(Type.PUNCTUATION, ')'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('x3')]),
            From('FROM', statements=[Identifier('tab1')]),
            Where('WHERE', statements=[
                Compare('x IN', statements=[
                    Sub('(', statements=[
                        Identifier('"78"'),
                        Comma(','),
                        Identifier('"d"'),
                    ])
                ])
            ])
        ],
        style=[
            'SELECT',
            '    x3',
            'FROM',
            '    tab1',
            'WHERE',
            '    x IN (',
            '        "78",',
            '        "d")',
            ''
        ])


@fixture
def select_with_group_and_having():
    return Data(
        sql='SELECT country FROM sales GROUP BY country, product HAVING product > 0',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, 'country'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'sales'),
            Token(Type.GROUP, 'GROUP BY'),
            Token(Type.STR, 'country'),
            Token(Type.PUNCTUATION, ','),
            Token(Type.STR, 'product'),
            Token(Type.HAVING, 'HAVING'),
            Token(Type.STR, 'product'),
            Token(Type.COMPARE, '>'),
            Token(Type.STR, '0'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('country')]),
            From('FROM', statements=[Identifier('sales')]),
            Group('GROUP BY', statements=[
                Identifier('country'),
                Comma(','),
                Identifier('product')
            ]),
            Having('HAVING', statements=[Compare('product > 0')])
        ],
        style=[
            'SELECT',
            '    country',
            'FROM',
            '    sales',
            'GROUP BY',
            '    country,',
            '    product',
            'HAVING',
            '    product > 0',
            ''
        ])


@fixture
def select_with_join_with_and():
    return Data(
        sql='',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'tab1'),
            Token(Type.JOIN, 'INNER JOIN'),
            Token(Type.STR, 'tab2'),
            Token(Type.KEYWORD, 'ON'),
            Token(Type.STR, 'tab1.id'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'tab2.id'),
            Token(Type.LINK, 'AND'),
            Token(Type.STR, 'tab1.id2'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'tab2.id2'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[
                Identifier('tab1'),
                Join('INNER JOIN'),
                Identifier('tab2'),
                Key('ON'),
                Compare('tab1.id = tab2.id'),
                Link('AND'),
                Compare('tab1.id2 = tab2.id2'),
            ]),
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    tab1',
            '    INNER JOIN tab2',
            '        ON tab1.id = tab2.id',
            '        AND tab1.id2 = tab2.id2',
            ''
        ])


@fixture
def select_with_complex_filter():
    return Data(
        sql='SELECT * FROM mart AS q WHERE m_id = "14" AND (qt IS NULL OR qt = 0)',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'mart AS q'),
            Token(Type.WHERE, 'WHERE'),
            Token(Type.STR, 'm_id'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, '"14"'),
            Token(Type.LINK, 'AND'),
            Token(Type.PUNCTUATION, '('),
            Token(Type.STR, 'qt'),
            Token(Type.COMPARE, 'IS'),
            Token(Type.KEYWORD, 'NULL'),
            Token(Type.LINK, 'OR'),
            Token(Type.STR, 'qt'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, '0'),
            Token(Type.PUNCTUATION, ')'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[Identifier('mart AS q')]),
            Where('WHERE', statements=[
                Compare('m_id = "14"'),
                Link('AND'),
                Sub('(', statements=[
                    Compare('qt IS NULL'),
                    Link('OR'),
                    Compare('qt = 0'),
                ])
            ])
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    mart AS q',
            'WHERE',
            '    m_id = "14"',
            '    AND (',
            '        qt IS NULL',
            '        OR qt = 0)',
            ''
        ])


@fixture
def select_with_sub_select_in_filter():
    return Data(
        sql='SELECT name, some_par1  FROM my_table WHERE  some_par1 IN (SELECT some_par1 FROM some_special_table)',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, 'name'),
            Token(Type.PUNCTUATION, ','),
            Token(Type.STR, 'some_par1'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'my_table'),
            Token(Type.WHERE, 'WHERE'),
            Token(Type.STR, 'some_par1'),
            Token(Type.COMPARE, 'IN'),
            Token(Type.PUNCTUATION, '('),
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, 'some_par1'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'some_special_table'),
            Token(Type.PUNCTUATION, ')'),
        ],
        statements=[
            Select('SELECT', statements=[
                Identifier('name'),
                Comma(','),
                Identifier('some_par1')
            ]),
            From('FROM', statements=[Identifier('my_table')]),
            Where('WHERE', statements=[
                Compare('some_par1 IN', statements=[
                    Sub('(', statements=[
                        Select('SELECT', statements=[Identifier('some_par1')]),
                        From('FROM',
                             statements=[Identifier('some_special_table')])
                    ]),
                ])
            ])
        ],
        style=[
            'SELECT',
            '    name,',
            '    some_par1',
            'FROM',
            '    my_table',
            'WHERE',
            '    some_par1 IN (',
            '        SELECT',
            '            some_par1',
            '        FROM',
            '            some_special_table)',
            ''
        ])


@fixture
def select_with_complex_having():
    return Data(
        sql='SELECT * FROM uiop AS s INNER JOIN rag AS r ON s.r_id = r.id GROUP BY s.id HAVING cnt > 0 AND NOT (min_number = 1 AND max_number = cnt)',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'uiop AS s'),
            Token(Type.JOIN, 'INNER JOIN'),
            Token(Type.STR, 'rag AS r'),
            Token(Type.KEYWORD, 'ON'),
            Token(Type.STR, 's.r_id'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'r.id'),
            Token(Type.GROUP, 'GROUP BY'),
            Token(Type.STR, 's.id'),
            Token(Type.HAVING, 'HAVING'),
            Token(Type.STR, 'cnt'),
            Token(Type.COMPARE, '>'),
            Token(Type.STR, '0'),
            Token(Type.LINK, 'AND'),
            Token(Type.KEYWORD, 'NOT'),
            Token(Type.PUNCTUATION, '('),
            Token(Type.STR, 'min_number'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, '1'),
            Token(Type.LINK, 'AND'),
            Token(Type.STR, 'max_number'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'cnt'),
            Token(Type.PUNCTUATION, ')'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[
                Identifier('uiop AS s'),
                Join('INNER JOIN'),
                Identifier('rag AS r'),
                Key('ON'),
                Compare('s.r_id = r.id'),
            ]),
            Group('GROUP BY', statements=[Identifier('s.id')]),
            Having('HAVING', statements=[
                Compare('cnt > 0'),
                Link('AND'),
                Key('NOT'),
                Sub('(', statements=[
                    Compare('min_number = 1'),
                    Link('AND'),
                    Compare('max_number = cnt')
                ])
            ])
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    uiop AS s',
            '    INNER JOIN rag AS r',
            '        ON s.r_id = r.id',
            'GROUP BY',
            '    s.id',
            'HAVING',
            '    cnt > 0',
            '    AND NOT (',
            '        min_number = 1',
            '        AND max_number = cnt)',
            ''
        ])


@fixture
def select_with_not_in_compare():
    return Data(
        sql='SELECT q FROM mart WHERE q IS NULL',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, 'q'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'mart'),
            Token(Type.WHERE, 'WHERE'),
            Token(Type.STR, 'q'),
            Token(Type.COMPARE, 'IS'),
            Token(Type.KEYWORD, 'NULL'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('q')]),
            From('FROM', statements=[Identifier('mart')]),
            Where('WHERE', statements=[Compare('q IS NULL')])
        ],
        style=[
            'SELECT',
            '    q',
            'FROM',
            '    mart',
            'WHERE',
            '    q IS NULL',
            ''
        ])


@fixture
def select_with_multiple_joins():
    return Data(
        sql='SELECT * FROM tab1 JOIN tab2 ON tab1.id = tab2.id JOIN tab3 ON tab2.id = tab3.id',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'tab1'),
            Token(Type.JOIN, 'JOIN'),
            Token(Type.STR, 'tab2'),
            Token(Type.KEYWORD, 'ON'),
            Token(Type.STR, 'tab1.id'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'tab2.id'),
            Token(Type.JOIN, 'JOIN'),
            Token(Type.STR, 'tab3'),
            Token(Type.KEYWORD, 'ON'),
            Token(Type.STR, 'tab2.id'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'tab3.id'),
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[
                Identifier('tab1'),
                Join('JOIN'),
                Identifier('tab2'),
                Key('ON'),
                Compare('tab1.id = tab2.id'),
                Join('JOIN'),
                Identifier('tab3'),
                Key('ON'),
                Compare('tab2.id = tab3.id')
            ])
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    tab1',
            '    JOIN tab2',
            '        ON tab1.id = tab2.id',
            '    JOIN tab3',
            '        ON tab2.id = tab3.id',
            ''
        ])


@fixture
def select_in_from():
    return Data(
        sql='SELECT * FROM (SELECT x FROM tab1) AS t',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.PUNCTUATION, '('),
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, 'x'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'tab1'),
            Token(Type.PUNCTUATION, ')'),
            Token(Type.STR, 'AS t')
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[
                Sub('(', statements=[
                    Select('SELECT', statements=[Identifier('x')]),
                    From('FROM', statements=[Identifier('tab1')])
                ]),
                Identifier('AS t')
            ])
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    (',
            '        SELECT',
            '            x',
            '        FROM',
            '            tab1) AS t',
            ''
        ])


@fixture
def select_in_from_and_join():
    return Data(
        sql='SELECT * FROM (SELECT x FROM tab1) AS t JOIN tab2 ON t.id = tab.id',
        tokens=[
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, '*'),
            Token(Type.FROM, 'FROM'),
            Token(Type.PUNCTUATION, '('),
            Token(Type.SELECT, 'SELECT'),
            Token(Type.STR, 'x'),
            Token(Type.FROM, 'FROM'),
            Token(Type.STR, 'tab1'),
            Token(Type.PUNCTUATION, ')'),
            Token(Type.STR, 'AS t'),
            Token(Type.JOIN, 'JOIN'),
            Token(Type.STR, 'tab2'),
            Token(Type.KEYWORD, 'ON'),
            Token(Type.STR, 't.id'),
            Token(Type.COMPARE, '='),
            Token(Type.STR, 'tab.id')
        ],
        statements=[
            Select('SELECT', statements=[Identifier('*')]),
            From('FROM', statements=[
                Sub('(', statements=[
                    Select('SELECT', statements=[Identifier('x')]),
                    From('FROM', statements=[Identifier('tab1')])
                ]),
                Identifier('AS t'),
                Join('JOIN'),
                Identifier('tab2'),
                Key('ON'),
                Compare('t.id = tab.id')
            ])
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    (',
            '        SELECT',
            '            x',
            '        FROM',
            '            tab1) AS t',
            '    JOIN tab2',
            '        ON t.id = tab.id',
            ''
        ])
