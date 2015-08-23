def args():
    X.objects.raw("""insert into x select * from k;""")
