# -*- coding: utf-8 -*-
"""
format-sql
Makes your SQL readable.

Copyright (c) 2015, Friedrich Paetzke (paetzke@fastmail.fm)
All rights reserved.

"""
from __future__ import print_function

import sys


def print_data(msg):
    print(msg)


def print_non_data(msg):
    print(msg, file=sys.stderr)
