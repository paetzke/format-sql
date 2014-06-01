# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from __future__ import unicode_literals

from format_sql.file_handling import (_format_py_text, _format_sql_text,
                                      _get_file_in_path, format_file)
from mock import patch


def test_find_no_files_in_folder_if_recursive_is_false(tmpdir):
    p = tmpdir.mkdir('sub').join('hello.py')
    p.write('content')

    results = _get_file_in_path(tmpdir.strpath, 'py', False)
    assert list(results) == []


def test_find_files_in_folder_if_recursive_is_true(tmpdir):
    p = tmpdir.mkdir('sub').join('hello.py')
    p.write('content')

    results = list(_get_file_in_path(tmpdir.strpath, 'py', True))
    assert len(results) == 1
    assert results[0].endswith('/sub/hello.py')


def test_format_sql_text():
    result = _format_sql_text('select * from tab')
    assert result == 'SELECT\n    *\nFROM\n    tab\n'


def test_dont_change_empty_file(tmpdir):
    pe = tmpdir.join('hello.py')
    pe.write('')
    format_file(pe.strpath, 'py')
    assert pe.read() == ''


def test_recognize_sql_in_assignment():
    content = '''def func():
    sql = """
select *
from my_table ;
    """

    return None
'''
    with patch('format_sql.file_handling.format_sql') as mocked_format_sql:
        _format_py_text(content)

        mocked_format_sql.assert_called_once_with('select * from my_table ;')


def test_recognize_sql_in_function_call():
    content = '''def func():
    sql.execute("""select *
from my_table
;
    """)

    print('')
    return None
'''
    with patch('format_sql.file_handling.format_sql') as mocked_format_sql:
        _format_py_text(content)

        mocked_format_sql.assert_called_once_with('select * from my_table ;')


def test_recognize_sql_without_semicolon():
    content = '''def func():
    sql.execute("""select *
from my_table
    """)

    print('')
    return None
'''

    with patch('format_sql.file_handling.format_sql') as mocked_format_sql:
        _format_py_text(content, with_semicolon=False)

        mocked_format_sql.assert_called_once_with('select * from my_table')
