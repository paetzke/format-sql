format-sql
==========

.. image:: https://travis-ci.org/paetzke/format-sql.svg?branch=master
  :target: https://travis-ci.org/paetzke/format-sql
.. image:: https://coveralls.io/repos/paetzke/format-sql/badge.png?branch=master
  :target: https://coveralls.io/r/paetzke/format-sql?branch=master
.. image:: https://pypip.in/v/format-sql/badge.png
  :target: https://pypi.python.org/pypi/format-sql/

format-sql is a tool to format SQL in your Python strings!

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
                LEFT JOIN x
                    ON x.id = sales.k
            GROUP BY
                country,
                product
            HAVING
                f > 7
                AND fk = 9
            LIMIT
                5
            ; """

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

You can try format-sql online: `http://paetzke.me/format-sql <http://paetzke.me/format-sql>`_.

Changes
-------

0.2.2
~~~~~

* Fix an issue with passing ``--types`` command line argument.

0.2.1
~~~~~

* Fix an issue with passing command line arguments.

0.2
~~~

* Add handling for unknown token sequences.
* Fix detecting special words. Word boundaries have been ignored.
* Single comparison in joins are printed on one line.
* Support ``LIKE`` and ``LIKE BINARY`` for comparison.

0.1
~~~

* Add parameter ``--no-semicolon`` to enable taking SQL queries without semicolon into account.

Copyright (c) 2014, Friedrich Paetzke (paetzke@fastmail.fm). All rights reserved.

