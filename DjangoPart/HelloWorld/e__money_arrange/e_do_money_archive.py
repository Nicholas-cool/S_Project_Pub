from django.http import HttpResponse
import sqlite3
import time
from datetime import datetime


def e_do_money_archive(request):

    # 创建数据库连接
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    archive_id = round(time.time())
    archive_time = datetime.now().strftime('%Y-%m-%d %H:%M')

    # 获取当前所有资金位置的资金量
    cur.execute(""" select name_en, money from e_money_position; """)
    cur_result = cur.fetchall()

    for _ in cur_result:
        cur.execute(""" 
            insert into e_money_archive (archive_id, archive_time, position, money) values (?, ?, ?, ?); 
        """, (archive_id, archive_time, _[0], _[1]))
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse("资金归档成功！")
