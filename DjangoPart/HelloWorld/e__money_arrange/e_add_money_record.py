from django.http import HttpResponse
import sqlite3


def e_add_money_record(request):
    """ 添加 资金记录条目 到数据库中 """

    record_name = request.POST.get('record_name')
    record_date = request.POST.get('record_date')
    record_inout = request.POST.get('record_inout')
    record_type = request.POST.get('record_type')
    record_position = request.POST.get('record_position')
    record_amount = request.POST.get('record_amount')

    record_desc = request.POST.get('record_desc')
    record_desc = record_desc if record_desc else 'No Description'

    ''' 添加到数据库 '''
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute(""" 
        INSERT INTO e_money_record (name, type, amount, inout, position, description, date_str) 
        VALUES (?, ?, ?, ?, ?, ?, ?) 
    """, (record_name, record_type, record_amount, record_inout, record_position, record_desc, record_date))
    conn.commit()

    ''' money_position 数额更新 '''
    cur.execute(""" select money from e_money_position where name_en = '%s'; """ % record_position)
    money_before = float(cur.fetchone()[0])

    if record_inout == 'in':
        money_after = round(money_before + float(record_amount), 2)
    elif record_inout == 'out':
        money_after = round(money_before - float(record_amount), 2)
    else:
        raise ValueError('inout error')

    cur.execute("""
        UPDATE e_money_position SET
        money = ?
        WHERE name_en = ?
    """, (str(money_after), record_position))
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse('资金记录 | 添加成功 ！')
