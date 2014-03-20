def func():
    sql.execute("""select *
from my_table as mt join ma_table as ta on ma.id = k.id
where idt=4 and ih in ('syds', 'sdsd');

    """)

    print('Yä$')
    return None
