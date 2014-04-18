# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
import os

from format_sql import format_file
from format_sql.format_sql import load_from_file


def get_test_file(filename):
    test_data = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    filename = os.path.join(test_data, 'tests/data', filename)
    return filename


def test_format_empty_file():
    filename = get_test_file('empty.py')
    format_file(filename)
    assert load_from_file(filename) == ''
