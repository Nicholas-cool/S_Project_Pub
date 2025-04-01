from django.http import HttpResponse
import sqlite3


def e_add_money_transfer_record(request):
    """ 添加 资金转移记录条目 到数据库中 """

    record_name = request.POST.get('record_name')
    record_date = request.POST.get('record_date')
    record_from_position = request.POST.get('record_from_position')
    record_to_position = request.POST.get('record_to_position')
    record_amount = request.POST.get('record_amount')
    record_fee = request.POST.get('record_fee')

    record_desc = request.POST.get('record_desc')
    record_desc = record_desc if record_desc else 'No Description'

    ''' 添加到数据库 '''
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute(""" 
        INSERT INTO e_money_record (name, type, amount, inout, position, description, date_str, fee) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
    """, (record_name, '转移', record_amount, 'transfer', record_from_position + '&&' + record_to_position,
          record_desc, record_date, record_fee))
    conn.commit()

    ''' money_position 数额更新 (from账户) '''
    cur.execute(""" select money from e_money_position where name_en = ?; """, (record_from_position, ))
    money_before = float(cur.fetchone()[0])
    money_after = round(money_before - float(record_amount) - float(record_fee), 2)
    cur.execute(""" 
        UPDATE e_money_position SET money = ? WHERE name_en = ?; 
    """, (str(money_after), record_from_position))
    conn.commit()

    ''' money_position 数额更新 (to账户) '''
    cur.execute(""" select money from e_money_position where name_en = ?; """, (record_to_position, ))
    money_before = float(cur.fetchone()[0])
    money_after = round(money_before + float(record_amount), 2)
    cur.execute("""
        UPDATE e_money_position SET money = ? WHERE name_en = ?;
    """, (str(money_after), record_to_position))
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse('资金转移记录 | 添加成功 ！')
