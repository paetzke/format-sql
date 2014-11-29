# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
import pytest
from format_sql.parser import InvalidSQL
from format_sql.shortcuts import format_sql


def test_():
    with pytest.raises(InvalidSQL):
        format_sql("Select x T K")
