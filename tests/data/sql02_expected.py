def func():
    sql = """
        SELECT
            *
        FROM
            my_table AS mt
            JOIN ma_table AS ta ON ma.id = k.id
        WHERE
            idt=4; """

    return None
