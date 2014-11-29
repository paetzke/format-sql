def args():
    item_count = X.objects.raw("""select * from k;""")
