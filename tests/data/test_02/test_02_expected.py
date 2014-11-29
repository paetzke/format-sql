def args():
    item_count = X.objects.raw("""
        SELECT
            *
        FROM
            k; """)
