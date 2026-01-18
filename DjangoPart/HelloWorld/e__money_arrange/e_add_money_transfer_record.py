from django.http import HttpResponse
from ..z__common.z_db_get_cursor import get_cursor


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

    with get_cursor() as cur:
        ''' 插入资金转移记录 '''
        cur.execute(""" 
            INSERT INTO e_money_record (name, type, amount, inout, position, description, date_str, fee) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
        """, (record_name, '转移', record_amount, 'transfer', record_from_position + '&&' + record_to_position,
              record_desc, record_date, record_fee))

        ''' money_position 数额更新 (from账户) '''
        cur.execute(""" select money from e_money_position where name_en = ?; """, (record_from_position, ))
        money_before = float(cur.fetchone()[0])
        money_after = round(money_before - float(record_amount) - float(record_fee), 2)
        cur.execute(""" 
            UPDATE e_money_position SET money = ? WHERE name_en = ?; 
        """, (str(money_after), record_from_position))

        ''' money_position 数额更新 (to账户) '''
        cur.execute(""" select money from e_money_position where name_en = ?; """, (record_to_position, ))
        money_before = float(cur.fetchone()[0])
        money_after = round(money_before + float(record_amount), 2)
        cur.execute("""
            UPDATE e_money_position SET money = ? WHERE name_en = ?;
        """, (str(money_after), record_to_position))

    return HttpResponse('资金转移记录 | 添加成功 ！')
