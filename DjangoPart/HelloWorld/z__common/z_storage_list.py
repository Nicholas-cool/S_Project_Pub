from django.http import HttpResponse
import sqlite3
import datetime


def z_storage_list(request):

    module = request.GET.get('module')
    item = request.GET.get('item')
    operation = request.GET.get('operation')
    value = request.GET.get('value')
    default_value = request.GET.get('default_value')

    # 创建数据库连接
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    date_today = datetime.datetime.now().strftime('%Y-%m-%d')

    if operation == 'get':
        cur.execute("""
            select value, update_time from z_storage_list
            where MODULE = ? and ITEM = ?;
        """, (module, item))
        result = cur.fetchone()

        if result[1] is None or result[1][:10] < date_today:
            # 如果过期，则返回默认值
            cur.execute("""
                update z_storage_list 
                set value = ?, update_time = ?
                where MODULE = ? and ITEM = ?;
            """, (default_value, date_today, module, item))
            conn.commit()
            result = (default_value, date_today)
        return_value = result[0]

    elif operation == 'set':
        cur.execute("""
            update z_storage_list 
            set value = ?, update_time = ?
            where MODULE = ? and ITEM = ?;
        """, (value, date_today, module, item))
        conn.commit()
        return_value = 'success'

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse(return_value)
