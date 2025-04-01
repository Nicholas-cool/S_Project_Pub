from django.http import HttpResponse
import sqlite3


def e_get_last_archive_time(request):

    # 创建数据库连接
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute(""" select archive_time from e_money_archive order by archive_time desc limit 1; """)
    archive_time = cur.fetchone()[0]

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse(archive_time)
