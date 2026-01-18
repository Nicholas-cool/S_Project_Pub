from django.http import HttpResponse
from ..z__common.z_db_get_cursor import get_cursor


def e_add_money_record(request):
    """ 添加 资金记录条目 到数据库中 """

    record_name = request.POST.get('record_name')
    record_date = request.POST.get('record_date')
    record_inout = request.POST.get('record_inout')
    record_type = request.POST.get('record_type')
    record_position = request.POST.get('record_position')
    record_ledger = request.POST.get('record_ledger')
    record_amount = request.POST.get('record_amount')

    record_desc = request.POST.get('record_desc')
    record_desc = record_desc if record_desc else 'No Description'

    with get_cursor() as cur:
        ''' 插入资金记录 '''
        cur.execute(""" 
            INSERT INTO e_money_record (name, type, amount, inout, position, description, date_str, ledger) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
        """, (record_name, record_type, record_amount, record_inout, record_position, record_desc,
              record_date, record_ledger))

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

    return HttpResponse('资金记录 | 添加成功 ！')
