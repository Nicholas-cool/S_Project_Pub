from django.http import HttpResponse
import sqlite3
import time


def e_add_ledger(request):
    ledger_name = request.POST.get('ledger_name')
    ledger_category = request.POST.get('ledger_category')

    ledger_desc = request.POST.get('ledger_desc')
    ledger_desc = ledger_desc if ledger_desc else 'No Description'

    # 创建数据库连接
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 添加记录信息
    cur.execute(""" 
        INSERT INTO e_money_ledger (ledger_id, name, desc, category) VALUES (?, ?, ?, ?) 
    """, (round(time.time()), ledger_name, ledger_desc, ledger_category))
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse('资金账本 | 添加成功 ！')
