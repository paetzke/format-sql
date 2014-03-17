format-sql
==========

.. image:: https://travis-ci.org/paetzke/format-sql.png?branch=master
  :target: https://travis-ci.org/paetzke/format-sql
.. image:: https://coveralls.io/repos/paetzke/format-sql/badge.png?branch=master
  :target: https://coveralls.io/r/paetzke/format-sql?branch=master
.. image:: https://pypip.in/v/format-sql/badge.png
  :target: https://pypi.python.org/pypi/format-sql/

Copyright (c) 2014, Friedrich Paetzke (f.paetzke@gmail.com)
All rights reserved.

format-sql is a tool to format SQL in your Python strings!

Install ``format-sql`` via ``pip``:

.. code:: bash

    $ pip install format-sql

You can then just call ``format-sql`` with files and directories:

.. code:: bash

    $ format-sql my_python_file.py my/python/dir/

An example:

.. code:: python

        sql = """
    select *
    from my_table as mt join ma_table as ta on ma.id = k.id
    where idt=4 and ih in ('syds', 'sdsd');
    
        """

Will result in:

.. code:: python

        sql = """
            SELECT
                *
            FROM
                my_table AS mt
                JOIN ma_table AS ta ON ma.id = k.id
            WHERE
                idt=4
                AND ih IN ('syds', 'sdsd'); """

This is an early version and work in progress. Don't expect too much right now.

