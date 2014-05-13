# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
import os

from format_sql.file_handling import (_format_sql_text, _get_file_in_path,
                                      format_file, load_from_file)


def get_test_file(filename):
    test_data = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    filename = os.path.join(test_data, 'tests/data', filename)
    return filename


def test_format_empty_file():
    filename = get_test_file('empty.py')
    format_file(filename, 'py')
    assert load_from_file(filename) == ''


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
    result = _format_sql_text('select * from table;')
    assert result == 'SELECT\n    *\nFROM\n    TABLE;\n'
