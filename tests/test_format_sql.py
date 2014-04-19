# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
import os

from format_sql.file_handling import format_text, load_from_file


def load_data(filename):
    test_data = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    filename = os.path.join(test_data, 'tests/data', filename)
    return load_from_file(filename)


def assert_files(filename1, filename2):
    content1 = load_data(filename1)
    content1 = format_text(content1)
    content2 = load_data(filename2)

    assert content1 == content2


def test_00():
    assert_files('sql00.py', 'sql00_expected.py')


def test_00_reapply():
    assert_files('sql00_expected.py', 'sql00_expected.py')


def test_01():
    assert_files('sql01.py', 'sql01_expected.py')


def test_01_reapply():
    assert_files('sql01_expected.py', 'sql01_expected.py')


def test_02():
    assert_files('sql02.py', 'sql02_expected.py')


def test_02_reapply():
    assert_files('sql02_expected.py', 'sql02_expected.py')


def test_03():
    assert_files('sql03.py', 'sql03_expected.py')


def test_03_reapply():
    assert_files('sql03_expected.py', 'sql03_expected.py')


def test_04():
    assert_files('sql04.py', 'sql04_expected.py')


def test_04_reapply():
    assert_files('sql04_expected.py', 'sql04_expected.py')


def test_05():
    assert_files('sql05.py', 'sql05_expected.py')


def test_05_reapply():
    assert_files('sql05_expected.py', 'sql05_expected.py')


def test_06():
    assert_files('sql06.py', 'sql06_expected.py')


def test_06_reapply():
    assert_files('sql06_expected.py', 'sql06_expected.py')
