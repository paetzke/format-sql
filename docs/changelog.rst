Changelog
=========


0.13 (UNRELEASED)
-----------------


0.12
----

* Fix: Parsing SQL after a function call in a join failed.

  .. code:: sql

    SELECT
        p.*
    FROM
        p1 AS p
        LEFT JOIN p2 AS r ON
            r.sk = CONCAT(p.x, '-!')
    WHERE
        1 = 1


* Parse ``case``

  .. code:: sql

    SELECT
        CASE
            WHEN spam THEN 1,
        CASE
            WHEN eggs THEN 1
            WHEN eggs3 THEN 2
            ELSE 0
    FROM
        table


0.11
----

* Parse ``like`` comparisons

  .. code:: sql

    SELECT
        *
    FROM
        xs
    WHERE
        x LIKE 'A%Z'


* Parse ``between`` comparisons

  .. code:: sql

    SELECT
        *
    FROM
        ys
    WHERE
        ys.id BETWEEN 91 AND 92


0.10
----

* Parse function calls in joins, for example:

  .. code:: sql

    FROM
        x
        JOIN r ON
            XYZ(r.id) = ABC(x.r)


* Parse ``SQL_CALC_FOUND_ROWS``

  .. code:: sql

    SELECT SQL_CALC_FOUND_ROWS
        *
    FROM
        tbl_name
    WHERE
        id > 100
    LIMIT 10;


0.9
---

* Parse INSERTs. This kind of INSERTs should work now:

  .. code:: sql

    INSERT INTO
        spam
    SELECT
        *
    FROM
        eggs


  .. code:: sql

    INSERT INTO
        table_name (col1, col2, 3)
    VALUES
         ("value!", value2, 3)


  .. code:: sql

    INSERT INTO
        table_name
    VALUES
        ("value!", value2, 3),
        ("1"),
        ("2")


* Parse functions with no arguments.

  .. code:: python

    sql = """ SELECT NOW() """


0.8
---

* Parse ``IS NOT NULL`` comparisions.

  .. code:: python

    sql = """ WHERE x IS NOT NULL """


* Parse ``IS NULL`` comparisions.

  .. code:: python

     sql = """ WHERE x IS NULL """


0.7
---

* Allow aliases in selects.

  .. code:: python

     sql = """ select x as y """


0.6
---

* Enabled single quotes as SQL string wrapper.
  So you can format double and single quoted SQL strings.

  .. code:: python

    sql = """ select x from y """
    sql `` ''' select x from y '''


* Fixed: Don't print ``--debug`` parameter value.
* Added ``--dry-run`` parameter. If ``--dry-run`` is set, no file will be altered but printed to STDOUT.
* Allow comparison of scalar with sub-select

  .. code:: python

    sql = """ where x = (select max(*) from k) """


0.5
---

* All given non-Python files are handled as SQL files.
  The ``--types`` parameter can be used to exclude certain file types.
* Added command line parameter ``--version`` to echo the current version.
* Added command line parameter ``--debug`` to print available debug output.


0.4
---

* ``Where`` conditions with string comparison are now processed correctly.
* Multiple statements in one SQL file can now be processed.
* Multiple statements in one Python string can now be processed.


0.3
---

* Package rewritten.


0.2.2
-----

* Fix an issue with passing ``--types`` command line argument.


0.2.1
-----

* Fix an issue with passing command line arguments.


0.2
---

* Add handling for unknown token sequences.
* Fix detecting special words. Word boundaries have been ignored.
* Single comparison in joins are printed on one line.
* Support ``LIKE`` and ``LIKE BINARY`` for comparison.


0.1
---

* Add parameter ``--no-semicolon`` to enable taking SQL queries without semicolon into account.
