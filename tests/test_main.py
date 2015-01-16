# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014-2015, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from format_sql.main import _get_args, handle_py_file, handle_sql_file, main

import pytest
from mock import call, patch

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest


@pytest.mark.parametrize('args, expected_paths, expected_types', [
    ('file1 file2 --types sql --types py', ['file1', 'file2'], ['sql', 'py']),
    ('file1 --types py --types sql', ['file1'], ['py', 'sql']),
    ('file1 file2 --types sql', ['file1', 'file2'], ['sql']),
    ('file1 file2', ['file1', 'file2'], ['py']),
    ('--types sql file2 file1', ['file2', 'file1'], ['sql']),
])
def test_get_args(args, expected_paths, expected_types):
    args = _get_args(args.split())

    assert args.paths == expected_paths
    assert args.types == expected_types
    assert not args.recursive


def test_find_sql_in_directory(test_data):
    args = '%s -r --types sql' % test_data.get_path('test_00')
    args = args.split()

    with patch('format_sql.main.handle_sql_file') as mocked_handle_sql_file:
        main(args)

        assert mocked_handle_sql_file.call_count == 3
        arguments = sorted([
            mocked_handle_sql_file.call_args_list[0][0][0],
            mocked_handle_sql_file.call_args_list[1][0][0],
            mocked_handle_sql_file.call_args_list[2][0][0],
        ])

    expected_paths = ['one.sql', 'two.sql', 'sub_dir/four.sql']

    for path, expected in zip_longest(arguments, sorted(expected_paths)):
        assert path.endswith('format-sql/tests/data/test_00/%s' % expected)


def test_find_py_in_directory(test_data):
    args = '%s -r --types py' % test_data.get_path('test_00')
    args = args.split()

    with patch('format_sql.main.handle_py_file') as mocked_handle_py_file:
        main(args)

        assert mocked_handle_py_file.call_count == 2
        arguments = sorted([
            mocked_handle_py_file.call_args_list[0][0][0],
            mocked_handle_py_file.call_args_list[1][0][0],
        ])

    expected_paths = ['three.py', 'sub_dir/five.py']

    for path, expected in zip_longest(arguments, sorted(expected_paths)):
        assert path.endswith('format-sql/tests/data/test_00/%s' % expected)


@pytest.mark.parametrize(('filename', 'expected_sql'), [
    ('test_01/test_00.sql', 'SELECT\n    x\nFROM\n    k'),
    ('test_01/test_01.sql', 'SELECT\n    x\nFROM\n    k;'),
])
def test_sql_file_formatting(test_data, filename, expected_sql):
    test_filename = test_data.get_path(filename)

    with patch('format_sql.main._write_back') as mocked_write_back:
        handle_sql_file(test_filename)

        assert mocked_write_back.call_args[0][1] == expected_sql


@pytest.mark.parametrize(('filename', 'expected_filename'), [
    ('test_02/test_00.py', 'test_02/test_00_expected.py'),
    ('test_02/test_01.py', 'test_02/test_01_expected.py'),
    ('test_02/test_02.py', 'test_02/test_02_expected.py'),
    ('test_02/test_03.py', 'test_02/test_03_expected.py'),
])
def test_py_file_formatting(test_data, filename, expected_filename):
    test_filename = test_data.get_path(filename)
    expected_filename = test_data.get_path(expected_filename)

    with patch('format_sql.main._write_back') as mocked_write_back:
        handle_py_file(test_filename)

        with open(expected_filename) as f:
            assert mocked_write_back.call_args[0][1] == f.read()


@pytest.mark.parametrize(('filename', 'expected_filename'), [
    ('test_03/before.sql', 'test_03/after.sql'),
])
def test_multiple_statements_per_sql_file(test_data, filename, expected_filename):
    test_filename = test_data.get_path(filename)
    expected_filename = test_data.get_path(expected_filename)

    with patch('format_sql.main._write_back') as mocked_write_back:
        handle_sql_file(test_filename)

        with open(expected_filename) as f:
            expected_data = f.read()

        assert mocked_write_back.call_count == 1
        assert mocked_write_back.call_args[0][1] == expected_data


def test_multiple_statements_in_python_string(test_data):
    test_filename = test_data.get_path('test_04/before.py')
    expected_filename = test_data.get_path('test_04/after.py')

    with patch('format_sql.main._write_back') as mocked_write_back:
        handle_py_file(test_filename)

        with open(expected_filename) as f:
            expected_data = f.read()

        assert mocked_write_back.call_count == 1
        assert mocked_write_back.call_args[0][1] == expected_data
