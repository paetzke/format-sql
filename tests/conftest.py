# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014-2015, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
import os
from collections import namedtuple

from format_sql.parser import (Condition, From, Func, GroupBy, Having,
                               Identifier, Insert, Is, Join, Limit, Link, Not,
                               Null, Number, On, Operator, OrderBy, Select,
                               Semicolon, Str, SubSelect, Values, Where)
from format_sql.tokenizer import Token
from pytest import fixture

Data = namedtuple('Data', ['sql', 'tokens', 'statements', 'style'])


@fixture
def test_data():
    class TestData:

        def get_path(self, path):
            return os.path.join(os.path.join(os.path.dirname(__file__), 'data'), path)

        def get_content(self, path):
            with open(self.get_path(path)) as f:
                return f.read()

    return TestData()


@fixture
def from_1():
    return Data(
        sql='From x',
        tokens=[
            Token(Token.FROM, 'From'),
            Token(Token.IDENTIFIER, 'x')
        ],
        statements=[
            From('From', values=[Identifier('x')])
        ],
        style=[
            'FROM',
            '    x'
        ])


@fixture
def from_2():
    return Data(
        sql='From x as t',
        tokens=[
            Token(Token.FROM, 'From'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.AS, 'as'),
            Token(Token.IDENTIFIER, 't')
        ],
        statements=[
            From('From', values=[Identifier('x', as_='as', alias='t')])
        ],
        style=[
            'FROM',
            '    x AS t'
        ])


@fixture
def from_3():
    return Data(
        sql='From x t, r As z',
        tokens=[
            Token(Token.FROM, 'From'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.IDENTIFIER, 't'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'r'),
            Token(Token.AS, 'As'),
            Token(Token.IDENTIFIER, 'z'),
        ],
        statements=[
            From('From', values=[
                Identifier('x', alias='t'),
                Identifier('r', as_='As', alias='z')])
        ],
        style=[
            'FROM',
            '    x t,',
            '    r AS z'
        ])


@fixture
def from_4():
    return Data(
        sql='From x t join r As z on t4.id1=z4.id2',
        tokens=[
            Token(Token.FROM, 'From'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.IDENTIFIER, 't'),
            Token(Token.JOIN, 'join'),
            Token(Token.IDENTIFIER, 'r'),
            Token(Token.AS, 'As'),
            Token(Token.IDENTIFIER, 'z'),
            Token(Token.ON, 'on'),
            Token(Token.IDENTIFIER, 't4.id1'),
            Token(Token.COMPARE, '='),
            Token(Token.IDENTIFIER, 'z4.id2'),
        ],
        statements=[
            From('From', values=[
                Identifier('x', alias='t'),
                Join('join'),
                Identifier('r', as_='As', alias='z'),
                On('on', values=[
                    Condition([Identifier('t4.id1'),
                               Operator('='),
                               Identifier('z4.id2')])
                ])
            ])
        ],
        style=[
            'FROM',
            '    x t',
            '    JOIN r AS z ON',
            '        t4.id1 = z4.id2'
        ])


@fixture
def from_5():
    return Data(
        sql='From x t join r As z on t.id1=z.id2 And t.id2=z.id3',
        tokens=[
            Token(Token.FROM, 'From'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.IDENTIFIER, 't'),
            Token(Token.JOIN, 'join'),
            Token(Token.IDENTIFIER, 'r'),
            Token(Token.AS, 'As'),
            Token(Token.IDENTIFIER, 'z'),
            Token(Token.ON, 'on'),
            Token(Token.IDENTIFIER, 't.id1'),
            Token(Token.COMPARE, '='),
            Token(Token.IDENTIFIER, 'z.id2'),
            Token(Token.LINK, 'And'),
            Token(Token.IDENTIFIER, 't.id2'),
            Token(Token.COMPARE, '='),
            Token(Token.IDENTIFIER, 'z.id3'),
        ],
        statements=[
            From('From', values=[
                Identifier('x', alias='t'),
                Join('join'),
                Identifier('r', as_='As', alias='z'),
                On('on', values=[
                    Condition([Identifier('t.id1'),
                               Operator('='),
                               Identifier('z.id2')]),
                    Link('And'),
                    Condition([Identifier('t.id2'),
                               Operator('='),
                               Identifier('z.id3')])
                ])
            ])
        ],
        style=[
            'FROM',
            '    x t',
            '    JOIN r AS z ON',
            '        t.id1 = z.id2',
            '        AND t.id2 = z.id3',
        ])


@fixture
def from_6():
    return Data(
        sql='From x t join r As z',
        tokens=[
            Token(Token.FROM, 'From'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.IDENTIFIER, 't'),
            Token(Token.JOIN, 'join'),
            Token(Token.IDENTIFIER, 'r'),
            Token(Token.AS, 'As'),
            Token(Token.IDENTIFIER, 'z'),
        ],
        statements=[
            From('From', values=[
                Identifier('x', alias='t'),
                Join('join'),
                Identifier('r', as_='As', alias='z')
            ])
        ],
        style=[
            'FROM',
            '    x t',
            '    JOIN r AS z',
        ])


@fixture
def func_1():
    return Data(
        sql='CONCAT(last_name,", ",first_name)',
        tokens=[
            Token(Token.FUNC, 'CONCAT'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.IDENTIFIER, 'last_name'),
            Token(Token.COMMA, ','),
            Token(Token.STR,  '", "'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'first_name'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Func('CONCAT', args=[Identifier('last_name'),
                                 Str('", "'),
                                 Identifier('first_name')]),
        ],
        style=[
            'CONCAT(last_name, ", ", first_name)'
        ])


@fixture
def func_2():
    return Data(
        sql='distinct(count(1))',
        tokens=[
            Token(Token.FUNC, 'distinct'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.FUNC, 'count'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.NUMBER, '1'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Func('distinct', [
                Func('count', [Number('1')])
            ]),
        ],
        style=[
            'DISTINCT(COUNT(1))'
        ])


@fixture
def func_3():
    return Data(
        sql='distinct(min(1, 3), max(0, 1))',
        tokens=[
            Token(Token.FUNC, 'distinct'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.FUNC, 'min'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.NUMBER, '1'),
            Token(Token.COMMA, ','),
            Token(Token.NUMBER, '3'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.COMMA, ','),
            Token(Token.FUNC, 'max'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.NUMBER, '0'),
            Token(Token.COMMA, ','),
            Token(Token.NUMBER, '1'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Func('distinct', [
                Func('min', [Number('1'), Number('3')]),
                Func('max', [Number('0'), Number('1')]),
            ]),
        ],
        style=[
            'DISTINCT(MIN(1, 3), MAX(0, 1))'
        ])


@fixture
def func_4():
    return Data(
        sql='Sum(price) as Summ',
        tokens=[
            Token(Token.FUNC, 'Sum'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.IDENTIFIER, 'price'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.AS, 'as'),
            Token(Token.IDENTIFIER, 'Summ')
        ],
        statements=[
            Func('Sum', args=[Identifier('price')], as_='as', alias='Summ'),
        ],
        style=[
            'SUM(price) AS Summ'
        ])


@fixture
def func_5():
    return Data(
        sql='Now()',
        tokens=[
            Token(Token.FUNC, 'Now'),
            Token(Token.PARENTHESIS_OPEN, '('),

            Token(Token.PARENTHESIS_CLOSE, ')')
        ],
        statements=[
            Func('Now', args=[]),
        ],
        style=[
            'NOW()'
        ])


@fixture
def group_by_1():
    return Data(
        sql='Group by col1',
        tokens=[
            Token(Token.GROUP_BY, 'Group by'),
            Token(Token.IDENTIFIER, 'col1'),
        ],
        statements=[
            GroupBy(values=[Identifier('col1')]),
        ],
        style=[
            'GROUP BY',
            '    col1'
        ])


@fixture
def group_by_2():
    return Data(
        sql='Group by 1',
        tokens=[
            Token(Token.GROUP_BY, 'Group by'),
            Token(Token.NUMBER, '1'),
        ],
        statements=[
            GroupBy(values=[Number('1')]),
        ],
        style=[
            'GROUP BY',
            '    1'
        ])


@fixture
def group_by_3():
    return Data(
        sql='Group by 1,col1',
        tokens=[
            Token(Token.GROUP_BY, 'Group by'),
            Token(Token.NUMBER, '1'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'col1'),
        ],
        statements=[
            GroupBy(values=[Number('1'), Identifier('col1')]),
        ],
        style=[
            'GROUP BY',
            '    1,',
            '    col1'
        ])


@fixture
def group_by_4():
    return Data(
        sql='Group by 1,col1 with rollup',
        tokens=[
            Token(Token.GROUP_BY, 'Group by'),
            Token(Token.NUMBER, '1'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'col1'),
            Token(Token.WITH_ROLLUP, 'with rollup'),
        ],
        statements=[
            GroupBy(values=[Number('1'), Identifier('col1')],
                    with_rollup='with rollup'),
        ],
        style=[
            'GROUP BY',
            '    1,',
            '    col1',
            '    WITH ROLLUP'
        ])


@fixture
def having_1():
    return Data(
        sql='having col1 !=1',
        tokens=[
            Token(Token.HAVING, 'having'),
            Token(Token.IDENTIFIER, 'col1'),
            Token(Token.COMPARE, '!='),
            Token(Token.NUMBER, '1'),
        ],
        statements=[
            Having('having',
                   [Condition([Identifier('col1'),
                               Operator('!='),
                               Number('1')])])
        ],
        style=[
            'HAVING',
            '    col1 != 1'
        ])


@fixture
def having_2():
    return Data(
        sql='having not count(1) !=1',
        tokens=[
            Token(Token.HAVING, 'having'),
            Token(Token.NOT, 'not'),
            Token(Token.FUNC, 'count'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.NUMBER, '1'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.COMPARE, '!='),
            Token(Token.NUMBER, '1'),
        ],
        statements=[
            Having('having',
                   [Condition([Not('not'),
                               Func('count', [Number('1')]),
                               Operator('!='),
                               Number('1')])])
        ],
        style=[
            'HAVING',
            '    NOT COUNT(1) != 1'
        ])


@fixture
def limit_1():
    return Data(
        sql='LIMIT 65',
        tokens=[
            Token(Token.LIMIT, 'LIMIT'),
            Token(Token.NUMBER, '65'),
        ],
        statements=[
            Limit(row_count=Number('65')),
        ],
        style=[
            'LIMIT 65',
        ])


@fixture
def limit_2():
    return Data(
        sql='LIMIT 65,66',
        tokens=[
            Token(Token.LIMIT, 'LIMIT'),
            Token(Token.NUMBER, '65'),
            Token(Token.COMMA, ','),
            Token(Token.NUMBER, '66'),
        ],
        statements=[
            Limit(row_count=Number('66'), offset=Number('65')),
        ],
        style=[
            'LIMIT 65, 66',
        ])


@fixture
def limit_3():
    return Data(
        sql='LIMIT 65 offset 66',
        tokens=[
            Token(Token.LIMIT, 'LIMIT'),
            Token(Token.NUMBER, '65'),
            Token(Token.IDENTIFIER, 'offset'),
            Token(Token.NUMBER, '66'),
        ],
        statements=[
            Limit(row_count=Number('65'), offset=Number('66'),
                  offset_keyword='offset'),
        ],
        style=[
            'LIMIT 65 OFFSET 66',
        ])


@fixture
def order_by_1():
    return Data(
        sql='order by 6',
        tokens=[
            Token(Token.ORDER_BY, 'order by'),
            Token(Token.NUMBER, '6'),
        ],
        statements=[
            OrderBy(values=[Number('6')]),
        ],
        style=[
            'ORDER BY',
            '    6'
        ])


@fixture
def order_by_2():
    return Data(
        sql='order by 6 Asc',
        tokens=[
            Token(Token.ORDER_BY, 'order by'),
            Token(Token.NUMBER, '6'),
            Token(Token.ASC, 'Asc'),
        ],
        statements=[
            OrderBy(values=[Number('6', sort='Asc')]),
        ],
        style=[
            'ORDER BY',
            '    6 ASC'
        ])


@fixture
def order_by_3():
    return Data(
        sql='order by 6 DESC',
        tokens=[
            Token(Token.ORDER_BY, 'order by'),
            Token(Token.NUMBER, '6'),
            Token(Token.DESC, 'DESC'),
        ],
        statements=[
            OrderBy(values=[Number('6', sort='DESC')]),
        ],
        style=[
            'ORDER BY',
            '    6 DESC'
        ])


@fixture
def order_by_4():
    return Data(
        sql='order by 6 DESC,col2 ASC',
        tokens=[
            Token(Token.ORDER_BY, 'order by'),
            Token(Token.NUMBER, '6'),
            Token(Token.DESC, 'DESC'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'col2'),
            Token(Token.ASC, 'ASC'),
        ],
        statements=[
            OrderBy(values=[Number('6', sort='DESC'),
                            Identifier('col2', sort='ASC')])
        ],
        style=[
            'ORDER BY',
            '    6 DESC,',
            '    col2 ASC'
        ])


@fixture
def select_1():
    return Data(
        sql='Select 1',
        tokens=[
            Token(Token.SELECT, 'Select'),
            Token(Token.NUMBER, '1'),
        ],
        statements=[
            Select('Select', [Number('1')]),
        ],
        style=[
            'SELECT',
            '    1'
        ])


@fixture
def select_2():
    return Data(
        sql='Select 1, col1',
        tokens=[
            Token(Token.SELECT, 'Select'),
            Token(Token.NUMBER, '1'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'col1'),
        ],
        statements=[
            Select('Select', [Number('1'), Identifier('col1')]),
        ],
        style=[
            'SELECT',
            '    1,',
            '    col1'
        ])


@fixture
def select_3():
    return Data(
        sql='Select 1, col1,min(3,4)',
        tokens=[
            Token(Token.SELECT, 'Select'),
            Token(Token.NUMBER, '1'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'col1'),
            Token(Token.COMMA, ','),
            Token(Token.FUNC, 'min'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.NUMBER, '3'),
            Token(Token.COMMA, ','),
            Token(Token.NUMBER, '4'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Select('Select', [
                Number('1'),
                Identifier('col1'),
                Func('min', [Number('3'), Number('4')])
            ]),
        ],
        style=[
            'SELECT',
            '    1,',
            '    col1,',
            '    MIN(3, 4)',
        ])


@fixture
def select_4():
    return Data(
        sql='Select 1 as 2',
        tokens=[
            Token(Token.SELECT, 'Select'),
            Token(Token.NUMBER, '1'),
            Token(Token.AS, 'as'),
            Token(Token.NUMBER, '2'),
        ],
        statements=[
            Select('Select',
                   [Number('1', as_='as', alias='2')])
        ],
        style=[
            'SELECT',
            '    1 AS 2'
        ])


@fixture
def where_1():
    return Data(
        sql='where x= 1',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.COMPARE, '='),
            Token(Token.NUMBER, '1')
        ],
        statements=[
            Where('where',
                  [Condition([Identifier('x'),
                              Operator('='),
                              Number('1')])])
        ],
        style=[
            'WHERE',
            '    x = 1'
        ])


@fixture
def where_2():
    return Data(
        sql='where not x= 1',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.NOT, 'not'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.COMPARE, '='),
            Token(Token.NUMBER, '1')
        ],
        statements=[
            Where('where', [
                Condition(
                    [
                        Not('not'),
                        Identifier('x'),
                        Operator('='),
                        Number('1')
                    ]
                )])
        ],
        style=[
            'WHERE',
            '    NOT x = 1'
        ])


@fixture
def where_3():
    return Data(
        sql='where not x= 1 and x != 3',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.NOT, 'not'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.COMPARE, '='),
            Token(Token.NUMBER, '1'),
            Token(Token.LINK, 'and'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.COMPARE, '!='),
            Token(Token.NUMBER, '3'),
        ],
        statements=[
            Where('where', [Condition([Not('not'),
                                       Identifier('x'),
                                       Operator('='),
                                       Number('1'),
                                       ]),
                            Link('and'),
                            Condition([Identifier('x'),
                                       Operator('!='),
                                       Number('3'),
                                       ]),
                            ])
        ],
        style=[
            'WHERE',
            '    NOT x = 1',
            '    AND x != 3'
        ])


@fixture
def where_4():
    return Data(
        sql='where x in (1, "3")',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.IN, 'in'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.NUMBER, '1'),
            Token(Token.COMMA, ','),
            Token(Token.STR, '"3"'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Where('where',
                  [
                      Condition(
                          [
                              Identifier('x'),
                              Operator('in'),
                              [
                                  Number('1'),
                                  Str('"3"')
                              ]
                          ])
                  ])
        ],
        style=[
            'WHERE',
            '    x IN (',
            '        1,',
            '        "3")'
        ])


@fixture
def where_5():
    return Data(
        sql='where x in (select * from k)',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.IN, 'in'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.SELECT, 'select'),
            Token(Token.IDENTIFIER, '*'),
            Token(Token.FROM, 'from'),
            Token(Token.IDENTIFIER, 'k'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Where('where',
                  [
                      Condition(
                          [
                              Identifier('x'),
                              Operator('in'),
                              SubSelect([Select('select', [Identifier('*')]),
                                         From('from', [Identifier('k')]
                                              )
                                         ])
                          ])
                  ])
        ],
        style=[
            'WHERE',
            '    x IN (',
            '        SELECT',
            '            *',
            '        FROM',
            '            k)'
        ])


@fixture
def where_6():
    return Data(
        sql='where x in (select max(1) from k)',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.IN, 'in'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.SELECT, 'select'),
            Token(Token.FUNC, 'max'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.NUMBER, '1'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.FROM, 'from'),
            Token(Token.IDENTIFIER, 'k'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Where('where',
                  [
                      Condition(
                          [
                              Identifier('x'),
                              Operator('in'),
                              SubSelect([
                                  Select('select',
                                         [Func('max', args=[Number('1')])]),
                                  From('from', [Identifier('k')])
                              ])
                          ])
                  ])
        ],
        style=[
            'WHERE',
            '    x IN (',
            '        SELECT',
            '            MAX(1)',
            '        FROM',
            '            k)'
        ])


@fixture
def where_7():
    return Data(
        sql='where x in (select * from k) Or c = 3',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.IN, 'in'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.SELECT, 'select'),
            Token(Token.IDENTIFIER, '*'),
            Token(Token.FROM, 'from'),
            Token(Token.IDENTIFIER, 'k'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.LINK, 'Or'),
            Token(Token.IDENTIFIER, 'c'),
            Token(Token.COMPARE, '='),
            Token(Token.NUMBER, '3'),
        ],
        statements=[
            Where('where',
                  [
                      Condition(
                          [
                              Identifier('x'),
                              Operator('in'),
                              SubSelect([Select('select', [Identifier('*')]),
                                         From('from', [Identifier('k')])
                                         ])
                          ]),
                      Link('Or'),
                      Condition([Identifier('c'),
                                 Operator('='),
                                 Number('3')])])
        ],
        style=[
            'WHERE',
            '    x IN (',
            '        SELECT',
            '            *',
            '        FROM',
            '            k)',
            '    OR c = 3'
        ])


@fixture
def where_8():
    return Data(
        sql='where x = "abc"',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.COMPARE, '='),
            Token(Token.STR, '"abc"')
        ],
        statements=[
            Where('where',
                  [Condition([Identifier('x'),
                              Operator('='),
                              Str('"abc"')])])
        ],
        style=[
            'WHERE',
            '    x = "abc"'
        ])


@fixture
def where_9():
    return Data(
        sql='where not x = "abc"',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.NOT, 'not'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.COMPARE, '='),
            Token(Token.STR, '"abc"')
        ],
        statements=[
            Where('where',
                  [Condition([Not('not'),
                              Identifier('x'),
                              Operator('='),
                              Str('"abc"')])])
        ],
        style=[
            'WHERE',
            '    NOT x = "abc"'
        ])


@fixture
def where_10():
    return Data(
        sql='where x = (select max(*) from k)',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.COMPARE, '='),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.SELECT, 'select'),
            Token(Token.FUNC, 'max'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.IDENTIFIER, '*'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.FROM, 'from'),
            Token(Token.IDENTIFIER, 'k'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Where('where', [
                Condition([
                    Identifier('x'),
                    Operator('='),
                    SubSelect([
                        Select('select', [Func('max', args=[Identifier('*')])]),
                        From('from', [Identifier('k')])
                    ])
                ])
            ])
        ],
        style=[
            'WHERE',
            '    x = (',
            '        SELECT',
            '            MAX(*)',
            '        FROM',
            '            k)'
        ])


@fixture
def where_11():
    return Data(
        sql='where x is null',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.IS, 'is'),
            Token(Token.NULL, 'null'),
        ],
        statements=[
            Where('where',
                  [Condition([Identifier('x'),
                              Is('is'),
                              Null('null')])])
        ],
        style=[
            'WHERE',
            '    x IS NULL'
        ])


@fixture
def where_12():
    return Data(
        sql='where x is not null',
        tokens=[
            Token(Token.WHERE, 'where'),
            Token(Token.IDENTIFIER, 'x'),
            Token(Token.IS, 'is'),
            Token(Token.NOT, 'not'),
            Token(Token.NULL, 'null'),
        ],
        statements=[
            Where('where',
                  [Condition([Identifier('x'),
                              Is('is'),
                              Not('not'),
                              Null('null')])])
        ],
        style=[
            'WHERE',
            '    x IS NOT NULL'
        ])


@fixture
def composition_1():
    return Data(
        sql='select * from k',
        tokens=[
            Token(Token.SELECT, 'select'),
            Token(Token.IDENTIFIER, '*'),
            Token(Token.FROM, 'from'),
            Token(Token.IDENTIFIER, 'k')
        ],
        statements=[
            Select('select', [Identifier('*')]),
            From('from', [Identifier('k')])
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    k'
        ]
    )


@fixture
def composition_2():
    return Data(
        sql='select * from k;',
        tokens=[
            Token(Token.SELECT, 'select'),
            Token(Token.IDENTIFIER, '*'),
            Token(Token.FROM, 'from'),
            Token(Token.IDENTIFIER, 'k'),
            Token(Token.SEMICOLON, ';'),
        ],
        statements=[
            Select('select', [Identifier('*')]),
            From('from', [Identifier('k')]),
            Semicolon(';'),
        ],
        style=[
            'SELECT',
            '    *',
            'FROM',
            '    k;',
        ]
    )


@fixture
def multiple_statements_1():
    return Data(
        sql='select t1.* from t1; select t2.* from t2',
        tokens=[
            Token(Token.SELECT, 'select'),
            Token(Token.IDENTIFIER, 't1.*'),
            Token(Token.FROM, 'from'),
            Token(Token.IDENTIFIER, 't1'),
            Token(Token.SEMICOLON, ';'),
            Token(Token.SELECT, 'select'),
            Token(Token.IDENTIFIER, 't2.*'),
            Token(Token.FROM, 'from'),
            Token(Token.IDENTIFIER, 't2'),
        ],
        statements=[
            Select('select', [Identifier('t1.*')]),
            From('from', [Identifier('t1')]),
            Semicolon(';'),
            Select('select', [Identifier('t2.*')]),
            From('from', [Identifier('t2')]),
        ],
        style=[
            'SELECT',
            '    t1.*',
            'FROM',
            '    t1;',
            '',
            '',
            'SELECT',
            '    t2.*',
            'FROM',
            '    t2',
        ]
    )


@fixture
def insert_1():
    return Data(
        sql='insert into table_name values ("value!", value2,3)',
        tokens=[
            Token(Token.INSERT, 'insert into'),
            Token(Token.IDENTIFIER, 'table_name'),
            Token(Token.VALUES, 'values'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.STR, '"value!"'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'value2'),
            Token(Token.COMMA, ','),
            Token(Token.NUMBER, '3'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Insert('insert into',
                   table='table_name',
                   values=Values('values', [[Str('"value!"'),
                                             Identifier('value2'),
                                             Number('3')]]))
        ],
        style=[
            'INSERT INTO',
            '    table_name',
            'VALUES',
            '    ("value!", value2, 3)'
        ])


@fixture
def insert_2():
    return Data(
        sql='insert into table_name values ("value!", value2,3), ("1"), ("2")',
        tokens=[
            Token(Token.INSERT, 'insert into'),
            Token(Token.IDENTIFIER, 'table_name'),
            Token(Token.VALUES, 'values'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.STR, '"value!"'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'value2'),
            Token(Token.COMMA, ','),
            Token(Token.NUMBER, '3'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.COMMA, ','),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.STR, '"1"'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.COMMA, ','),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.STR, '"2"'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Insert('insert into',
                   table='table_name',
                   values=Values('values',
                                 [[Str('"value!"'),
                                   Identifier('value2'),
                                   Number('3')],
                                  [Str('"1"')],
                                  [Str('"2"')]]))
        ],
        style=[
            'INSERT INTO',
            '    table_name',
            'VALUES',
            '    ("value!", value2, 3),',
            '    ("1"),',
            '    ("2")'
        ])


@fixture
def insert_3():
    return Data(
        sql='insert into table_name (col1, col2, 3) values ("value!", value2,3)',
        tokens=[
            Token(Token.INSERT, 'insert into'),
            Token(Token.IDENTIFIER, 'table_name'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.IDENTIFIER, 'col1'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'col2'),
            Token(Token.COMMA, ','),
            Token(Token.NUMBER, '3'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
            Token(Token.VALUES, 'values'),
            Token(Token.PARENTHESIS_OPEN, '('),
            Token(Token.STR, '"value!"'),
            Token(Token.COMMA, ','),
            Token(Token.IDENTIFIER, 'value2'),
            Token(Token.COMMA, ','),
            Token(Token.NUMBER, '3'),
            Token(Token.PARENTHESIS_CLOSE, ')'),
        ],
        statements=[
            Insert('insert into',
                   table='table_name',
                   values=Values('values', [[Str('"value!"'),
                                             Identifier('value2'),
                                             Number('3')]]),
                   cols=[Identifier('col1'),
                         Identifier('col2'),
                         Number('3')]
                   )
        ],
        style=[
            'INSERT INTO',
            '    table_name (col1, col2, 3)',
            'VALUES',
            '    ("value!", value2, 3)'
        ])


@fixture
def insert_4():
    return Data(
        sql='INSERT INTO spam SELECT * FROM eggs',
        tokens=[
            Token(Token.INSERT, 'INSERT INTO'),
            Token(Token.IDENTIFIER, 'spam'),
            Token(Token.SELECT, 'SELECT'),
            Token(Token.IDENTIFIER, '*'),
            Token(Token.FROM, 'FROM'),
            Token(Token.IDENTIFIER, 'eggs'),
        ],
        statements=[
            Insert('INSERT INTO',
                   table='spam',
                   select=[
                       Select('SELECT', [Identifier('*')]),
                       From('FROM', [Identifier('eggs')])
                   ])
        ],
        style=[
            'INSERT INTO',
            '    spam',
            'SELECT',
            '    *',
            'FROM',
            '    eggs'
        ])
