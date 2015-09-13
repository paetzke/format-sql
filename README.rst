format-sql
==========

.. image:: https://travis-ci.org/paetzke/format-sql.svg?branch=master
  :target: https://travis-ci.org/paetzke/format-sql
.. image:: https://coveralls.io/repos/paetzke/format-sql/badge.svg?branch=master
  :target: https://coveralls.io/r/paetzke/format-sql?branch=master
.. image:: https://badge.fury.io/py/format-sql.svg
  :target: https://pypi.python.org/pypi/format-sql/
.. image:: https://readthedocs.org/projects/format-sql/badge/?version=latest
  :target: https://readthedocs.org/projects/format-sql/?badge=latest

Makes your SQL readable.

.. image:: https://paetzke.me/static/images/format-sql.gif

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
    usage: format-sql [-h] [--types TYPES] [-r] [--no-semicolon] [--version]
                      [--debug] [--dry-run]
                      paths [paths ...]
    
    positional arguments:
      paths
    
    optional arguments:
      -h, --help       show this help message and exit
      --types TYPES    Only process these given file types.
      -r, --recursive  Process files found in subdirectories.
      --no-semicolon   Try to detect SQL queries with no trailing semicolon.
      --version        show program's version number and exit
      --debug          Print available debug information.
      --dry-run        Print the altered output and do not change the file.

For example:

.. code:: bash

    $ format-sql my-file.py

Or recursively with directory:

.. code:: bash

    $ format-sql -r my-directory/

You can try format-sql online: `http://format-sql.de <http://format-sql.de>`_.

