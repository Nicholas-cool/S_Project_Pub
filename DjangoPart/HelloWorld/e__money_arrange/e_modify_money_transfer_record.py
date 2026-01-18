from django.http import HttpResponse
from ..z__common.z_db_get_cursor import get_cursor
from .e_modify_money_record import recover_inout_impact, recover_transfer_impact


def e_modify_money_transfer_record(request):
    """ 修改 资金转移记录条目；若原记录为普通（in/out），则回滚普通影响并按转移记录重放 """

    record_id = request.POST.get('record_id')
    record_name = request.POST.get('record_name')
    record_date = request.POST.get('record_date')
    record_from_position = request.POST.get('record_from_position')
    record_to_position = request.POST.get('record_to_position')
    record_amount = request.POST.get('record_amount')
    record_fee = request.POST.get('record_fee')
    record_ledger = request.POST.get('record_ledger')
    record_mode = request.POST.get('record_mode')

    record_desc = request.POST.get('record_desc')
    record_desc = record_desc if record_desc else 'No Description'

    origin_type = request.POST.get('record_origin_type')
    assert origin_type in ['in', 'out', 'transfer'], "Invalid origin_type"

    ''' 数据库信息修改 '''
    # 获取原记录信息
    # TODO: 如果在归档时间之前，不允许对金额等信息修改
    with get_cursor() as cur:
        cur.execute(""" SELECT inout FROM e_money_record WHERE id = ?;""", (record_id,))
        before_inout = cur.fetchone()[0]
        assert origin_type == before_inout

    # money_position 数据库数额更新（原记录退回）
    if before_inout == 'transfer':
        recover_transfer_impact(record_id)
    else:
        recover_inout_impact(record_id)

    with get_cursor() as cur:
        # 修改 money_record 记录信息
        cur.execute("""
            UPDATE e_money_record SET
            name = ?,
            type = ?,
            amount = ?,
            inout = ?,
            position = ?,
            description = ?,
            date_str = ?,
            fee = ?,
            status = 'good',
            ledger = ?,
            record_mode = ?
            WHERE id = ?;
        """, (record_name, '转移', record_amount, 'transfer', record_from_position + '&&' + record_to_position,
              record_desc, record_date, record_fee, record_ledger, record_mode, record_id))

        # money_position 数据库数额更新
        cur.execute(""" SELECT money FROM e_money_position WHERE name_en = ?; """, (record_from_position,))
        money_before = float(cur.fetchone()[0])
        money_after = round(money_before - float(record_amount) - float(record_fee), 2)
        cur.execute("""
            UPDATE e_money_position
            SET money = ?
            WHERE name_en = ?
        """, (str(money_after), record_from_position))

        cur.execute(""" SELECT money FROM e_money_position WHERE name_en = ?; """, (record_to_position,))
        money_before = float(cur.fetchone()[0])
        money_after = round(money_before + float(record_amount), 2)
        cur.execute("""
            UPDATE e_money_position 
            SET money = ? 
            WHERE name_en = ?
        """, (str(money_after), record_to_position))

    # 返回不同提示
    if before_inout == 'transfer':
        return HttpResponse('资金转移记录 | 信息修改成功 ！')
    else:
        return HttpResponse('资金记录 | 类型由 普通 -> 转移，信息修改成功 ！')
