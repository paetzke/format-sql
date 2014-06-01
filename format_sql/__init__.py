# -*- coding: utf-8 -*-
"""
format-sql

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from .file_handling import format_file
from .parser import (Comma, Compare, From, Group, Having, Identifier, Join, Key,
                     Limit, Link, Select, Statement, Sub, Where)
from .shortcuts import format_sql

__version__ = '0.1.0'
__author__ = 'Friedrich Paetzke'
__license__ = 'BSD'
__copyright__ = 'Copyright 2014 Friedrich Paetzke'
