sql = """ SELECT country, product, SUM(profit) FROM
sales   left join x on x.id=sales.k GROUP BY country,
product having f > 7 and fk=9 limit 5;    """
