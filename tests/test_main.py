# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
import pytest
from format_sql.main import _get_args, main

try:
    from unittest.mock import call, patch
except ImportError:
    from mock import call, patch


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


def test_args_recursive_is_active():
    args = 'file1 -r'.split()
    args = _get_args(args)

    assert args.paths == ['file1']
    assert args.types == ['py']
    assert args.recursive


def test_args_has_no_semicolon():
    args = 'file1 --no-semicolon'.split()
    args = _get_args(args)

    assert args.no_semicolon


def test_args_default_has_semicolon():
    args = 'file1'.split()
    args = _get_args(args)

    assert not args.no_semicolon


def test_main_args():
    args = 'file1 file2 --types sql'.split()

    with patch('format_sql.main._get_file_in_path') as mocked_get_file:
        main(args)
        assert mocked_get_file.call_args_list == [call('file1', 'sql', False),
                                                  call('file2', 'sql', False)]


@pytest.mark.parametrize('args, file_content, expected_output', [
    ('file1 --types sql', 'select * from tabl',
     'SELECT\n    *\nFROM\n    tabl\n'),
    ('file1', 'a = """select * from tabl;"""',
     'a = """\n    SELECT\n        *\n    FROM\n        tabl\n    ; """'),
])
@patch('format_sql.main._get_file_in_path')
@patch('format_sql.file_handling.load_from_file')
@patch('format_sql.file_handling.write_file')
def test_main_args3(mocked_write_file, mocked_load_from_file, mocked_get_file, args, file_content, expected_output):
    mocked_get_file.return_value = ['file1']
    mocked_load_from_file.return_value = file_content

    main(args.split())
    mocked_load_from_file.assert_called_once()
    mocked_write_file.assert_called_once_with('file1', expected_output)
