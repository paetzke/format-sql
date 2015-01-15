format-sql
==========

.. image:: https://travis-ci.org/paetzke/format-sql.svg?branch=master
  :target: https://travis-ci.org/paetzke/format-sql
.. image:: https://coveralls.io/repos/paetzke/format-sql/badge.png?branch=master
  :target: https://coveralls.io/r/paetzke/format-sql?branch=master
.. image:: https://pypip.in/v/format-sql/badge.png
  :target: https://pypi.python.org/pypi/format-sql/

Makes your SQL readable.

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
                LEFT JOIN x ON
                    x.id = sales.k
            GROUP BY
                country,
                product
            HAVING
                f > 7
                AND fk = 9
            LIMIT 5; """

Install ``format-sql`` via ``pip``:

.. code:: bash

    $ pip install format-sql

You can then just call ``format-sql`` with files and directories:

.. code:: bash

    $ format-sql -h
    usage: format-sql [-h] [--types {py,sql}] [-r] [--no-semicolon]
                      paths [paths ...]
    
    positional arguments:
      paths
    
    optional arguments:
      -h, --help        show this help message and exit
      --types {py,sql}  Process given file types. Default value is "py".
      -r, --recursive   Process files found in subdirectories.
      --no-semicolon    Try to detect SQL queries with no trailing semicolon.

For example:

.. code:: bash

    $ format-sql my-file.py

Or recursively with directory:

.. code:: bash

    $ format-sql -r my-directory/

You can try format-sql online: `https://paetzke.me/format-sql <https://paetzke.me/format-sql>`_.

