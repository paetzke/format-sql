# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
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


def test_16():
    sql = 'SELECT country, product, SUM(profit) FROM sales GROUP BY country, product;'
    expected = '\n'.join([
        'SELECT',
        '    country,',
        '    product,',
        '    SUM(profit)',
        'FROM',
        '    sales',
        'GROUP BY',
        '    country,',
        '    product;',
    ])

    assert_format(sql, expected)


def test_17():
    sql = 'SELECT name, some_par1 FROM zauber_table WHERE some_par1 < ALL ( select some_par1 FROM some_special_table group by x)'
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
        '            some_special_table',
        '        GROUP BY',
        '            x)',
    ])

    assert_format(sql, expected)


def test_18():
    sql = 'SELECT country, product, SUM(profit) FROM sales GROUP BY country, product having product > 0;'
    expected = '\n'.join([
        'SELECT',
        '    country,',
        '    product,',
        '    SUM(profit)',
        'FROM',
        '    sales',
        'GROUP BY',
        '    country,',
        '    product',
        'HAVING',
        '    product > 0;',
    ])

    assert_format(sql, expected)


def test_19():
    sql = 'SELECT country, product, SUM(profit) FROM sales GROUP BY country, product having f > 7 and fk=9;'
    expected = '\n'.join([
        'SELECT',
        '    country,',
        '    product,',
        '    SUM(profit)',
        'FROM',
        '    sales',
        'GROUP BY',
        '    country,',
        '    product',
        'HAVING',
        '    f > 7',
        '    AND fk = 9;',
    ])

    assert_format(sql, expected)


def test_20():
    sql = 'SELECT country, product, SUM(profit) FROM sales GROUP BY country, product having f > 7 and fk=9 limit 5;'
    expected = '\n'.join([
        'SELECT',
        '    country,',
        '    product,',
        '    SUM(profit)',
        'FROM',
        '    sales',
        'GROUP BY',
        '    country,',
        '    product',
        'HAVING',
        '    f > 7',
        '    AND fk = 9',
        'LIMIT 5;',
    ])

    assert_format(sql, expected)


def test_21():
    sql = 'SELECT * FROM my_table limit 65'
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    my_table',
        'LIMIT 65',
    ])

    assert_format(sql, expected)


def test_22():
    sql = 'SELECT * FROM my_table limit 65,90'
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    my_table',
        'LIMIT 65, 90',
    ])

    assert_format(sql, expected)


def test_23():
    sql = 'SELECT country, product, SUM(profit) FROM sales   left join x on x.id=sales.k GROUP BY country, product having f > 7 and fk=9 limit 5;'
    expected = '\n'.join([
        'SELECT',
        '    country,',
        '    product,',
        '    SUM(profit)',
        'FROM',
        '    sales',
        '    LEFT JOIN x ON x.id = sales.k',
        'GROUP BY',
        '    country,',
        '    product',
        'HAVING',
        '    f > 7',
        '    AND fk = 9',
        'LIMIT 5;',
    ])

    assert_format(sql, expected)


def test_24():
    sql = 'SELECT df.*, dt.p FROM my_table '
    expected = '\n'.join([
        'SELECT',
        '    df.*,',
        '    dt.p',
        'FROM',
        '    my_table',
    ])

    assert_format(sql, expected)


def test_25():
    sql = 'SELECT x.country, f.product, SUM(fp.profit) FROM sales;'
    expected = '\n'.join([
        'SELECT',
        '    x.country,',
        '    f.product,',
        '    SUM(fp.profit)',
        'FROM',
        '    sales;',
    ])

    assert_format(sql, expected)


def test_26():
    sql = 'SELECT x.country, f.product FROM sales;'
    expected = '\n'.join([
        'SELECT',
        '    x.country,',
        '    f.product',
        'FROM',
        '    sales;',
    ])

    assert_format(sql, expected)


def test_27():
    sql = 'SELECT x.country, f.product FROM sales WHERE x.t=5 oR tz.oi=  "s";'
    expected = '\n'.join([
        'SELECT',
        '    x.country,',
        '    f.product',
        'FROM',
        '    sales',
        'WHERE',
        '    x.t = 5',
        '    OR tz.oi = "s";',
    ])

    assert_format(sql, expected)


def test_28():
    sql = 'SELECT country, product, SUM(profit) FROM sales   left join x on x.id=sales.k order BY k asc, k.lk DESC limit 5;'
    expected = '\n'.join([
        'SELECT',
        '    country,',
        '    product,',
        '    SUM(profit)',
        'FROM',
        '    sales',
        '    LEFT JOIN x ON x.id = sales.k',
        'ORDER BY',
        '    k ASC,',
        '    k.lk DESC',
        'LIMIT 5;',
    ])

    assert_format(sql, expected)


def test_29():
    sql = 'SELECT country, product, SUM(profit) FROM sales   left join x on x.id=sales.k GROUP BY country, product having f > 7 and fk=9 order BY k asc limit 5;'
    expected = '\n'.join([
        'SELECT',
        '    country,',
        '    product,',
        '    SUM(profit)',
        'FROM',
        '    sales',
        '    LEFT JOIN x ON x.id = sales.k',
        'GROUP BY',
        '    country,',
        '    product',
        'HAVING',
        '    f > 7',
        '    AND fk = 9',
        'ORDER BY',
        '    k ASC',
        'LIMIT 5;',
    ])

    assert_format(sql, expected)


def test_30():
    sql = 'SELECT plo.md,sp.condition,sp.rice FROM cot_iu sp JOIN loooc plo ON plo.id = sp.popop_on_loc_u_t WHERE plo.loc_u_t = %(some_thing)s AND sp.rice IS NOT NULL'
    expected = '\n'.join([
        'SELECT',
        '    plo.md,',
        '    sp.condition,',
        '    sp.rice',
        'FROM',
        '    cot_iu sp',
        '    JOIN loooc plo ON plo.id = sp.popop_on_loc_u_t',
        'WHERE',
        '    plo.loc_u_t = %(some_thing)s',
        '    AND sp.rice IS NOT NULL',
    ])

    assert_format(sql, expected)


def test_31():
    sql = 'select * from tbl1 inner join tlb2 on tbl1.o=tbl2.p'
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    tbl1',
        '    INNER JOIN tlb2 ON tbl1.o = tbl2.p',
    ])

    assert_format(sql, expected)


def test_32():
    sql = 'SELECT * FROM uiop AS s GROUP BY s.id HAVING NOT (min_number = 1 AND max_number = cnt)'
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    uiop AS s',
        'GROUP BY',
        '    s.id',
        'HAVING',
        '    NOT (',
        '        min_number = 1',
        '        AND max_number = cnt)',
    ])

    assert_format(sql, expected)


def test_33():
    sql = 'SELECT * FROM uiop AS s INNER JOIN rag AS r ON s.r_id = r.id GROUP BY s.id HAVING cnt > 0 AND NOT (min_number = 1 AND max_number = cnt)'
    expected = '\n'.join([
        'SELECT',
        '    *',
        'FROM',
        '    uiop AS s',
        '    INNER JOIN rag AS r ON s.r_id = r.id',
        'GROUP BY',
        '    s.id',
        'HAVING',
        '    cnt > 0',
        '    AND NOT (',
        '        min_number = 1',
        '        AND max_number = cnt)',
    ])

    assert_format(sql, expected)
