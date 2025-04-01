from django.http import HttpResponse
import sqlite3
import datetime
import random


def z_get_quotation(request):
    # quotation 类型
    quotation_type = request.GET.get('quotation_type', 'all')

    # 创建数据库连接，返回连接对象 conn，返回游标 cur
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 查询该记录的信息，返回列表数据
    if quotation_type != 'all':
        cur.execute(" select CONTENT FROM quotations WHERE TYPE = '%s'; " % quotation_type)
    else:
        cur.execute(" select CONTENT FROM quotations; ")

    all_record = [_[0] for _ in cur.fetchall()]

    # one_quotation = random.choice(all_record)    # 随机选择一条语句
    # 按照每年 365 天，每一天对应一条语句
    tm_yday = int(datetime.datetime.now().timetuple().tm_yday)
    one_quotation = all_record[tm_yday % len(all_record)]

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse(one_quotation)
