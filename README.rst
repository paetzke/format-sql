format-sql
==========

.. image:: https://travis-ci.org/paetzke/format-sql.svg?branch=master
  :target: https://travis-ci.org/paetzke/format-sql
.. image:: https://coveralls.io/repos/paetzke/format-sql/badge.png?branch=master
  :target: https://coveralls.io/r/paetzke/format-sql?branch=master
.. image:: https://pypip.in/v/format-sql/badge.png
  :target: https://pypi.python.org/pypi/format-sql/

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm)
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

        sql = """ SELECT country, product, SUM(profit) FROM
    sales   left join x on x.id=sales.k GROUP BY country,
    product having f > 7 and fk=9 limit 5;    """

Will result in:

.. code:: python

        sql = """
            SELECT
                country,
                product,
                SUM(profit)
            FROM
                sales
                LEFT JOIN x ON x.id = sales.k
            GROUP BY
                country,
                product
            HAVING
                f > 7
                AND fk = 9
            LIMIT 5; """

This is an early version and work in progress. Don't expect too much right now.

