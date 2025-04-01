from django.http import HttpResponse
import sqlite3


def e_modify_record_ledger(request):
    ledger_id = request.POST.get('ledger_id')
    record_ids = eval(request.POST.get('record_ids'))

    ''' 数据库信息修改 '''
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 修改 money_record 记录信息
    for record_id in record_ids:
        cur.execute(""" 
            UPDATE e_money_record SET
            LEDGER = '%s'
            WHERE id = '%s';
        """ % (ledger_id, record_id))
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse('资金记录 | 加入账本成功 ！')
