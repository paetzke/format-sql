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
