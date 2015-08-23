def args():
    X.objects.raw("""
        INSERT INTO
            x
        SELECT
            *
        FROM
            k; """)
