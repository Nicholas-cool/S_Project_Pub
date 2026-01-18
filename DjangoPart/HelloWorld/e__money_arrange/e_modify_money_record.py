from django.http import HttpResponse
from ..z__common.z_db_get_cursor import get_cursor


def recover_inout_impact(record_id):
    with get_cursor() as cur:
        # 获取原记录信息
        cur.execute(""" SELECT position, inout, amount FROM e_money_record WHERE id = ?; """, (record_id,))
        before_position, before_inout, before_amount = cur.fetchone()

        # money_position 数据库数额更新（原记录退回）
        before_amount = -1 * float(before_amount) if before_inout == 'in' else float(before_amount)
        cur.execute(""" select money from e_money_position where name_en = ?; """, (before_position,))
        money_before = float(cur.fetchone()[0])
        money_after = round(money_before + float(before_amount), 2)
        cur.execute("""
            UPDATE e_money_position SET
            money = ?
            WHERE name_en = ?
        """, (str(money_after), before_position))


def recover_transfer_impact(record_id):
    with get_cursor() as cur:
        # 获取原记录信息
        cur.execute("""
            SELECT position, inout, amount, fee
            FROM e_money_record
            WHERE id = ?;
        """, (record_id,))
        before_position, before_inout, before_amount, before_fee = cur.fetchone()

        # money_position 数据库数额更新（原记录退回）
        before_position_from, before_position_to = before_position.split('&&')

        cur.execute(""" SELECT money FROM e_money_position WHERE NAME_EN = ?; """, (before_position_from,))
        money_before = float(cur.fetchone()[0])
        money_after = round(money_before + float(before_amount) + float(before_fee), 2)
        cur.execute("""
            UPDATE e_money_position SET
            money = ?
            WHERE name_en = ?
        """, (str(money_after), before_position_from))

        cur.execute(""" SELECT money FROM e_money_position WHERE name_en = ?; """, (before_position_to,))
        money_before = float(cur.fetchone()[0])
        money_after = round(money_before - float(before_amount), 2)
        cur.execute("""
            UPDATE e_money_position SET 
            money = ?
            WHERE name_en = ?
        """, (str(money_after), before_position_to))


def e_modify_money_record(request):
    """ 修改 资金记录条目 到数据库中（若原记录为 transfer，则回滚转移影响并按普通记录重放） """

    record_id = request.POST.get('record_id')
    record_name = request.POST.get('record_name')
    record_date = request.POST.get('record_date')
    record_inout = request.POST.get('record_inout')
    record_type = request.POST.get('record_type')
    record_position = request.POST.get('record_position')
    record_amount = request.POST.get('record_amount')

    record_desc = request.POST.get('record_desc')
    record_desc = record_desc if record_desc else 'No Description'

    record_mode = request.POST.get('record_mode')
    record_ledger = request.POST.get('record_ledger')

    origin_type = request.POST.get('record_origin_type')
    assert origin_type in ['in', 'out', 'transfer'], "Invalid origin_type"

    ''' 数据库信息修改 '''
    # 获取原记录信息
    # TODO: 如果在归档时间之前，不允许对金额等信息修改
    with get_cursor() as cur:
        cur.execute(""" SELECT inout FROM e_money_record WHERE id = ?; """, (record_id,))
        before_inout = cur.fetchone()[0]
        assert origin_type == before_inout

    # money_position 数据库数额更新（原记录退回）
    if before_inout == 'transfer':
        recover_transfer_impact(record_id)
    else:
        recover_inout_impact(record_id)

    with get_cursor() as cur:
        # 修改 money_record 记录信息（同时把 fee 清空）
        cur.execute("""
            UPDATE e_money_record SET
            name = ?,
            type = ?,
            amount = ?,
            inout = ?,
            position = ?,
            description = ?,
            date_str = ?,
            fee = '',
            status = 'good',
            record_mode = ?,
            ledger = ?
            WHERE id = ?;
        """, (record_name, record_type, record_amount, record_inout, record_position, record_desc, record_date,
              record_mode, record_ledger, record_id))

        # money_position 数据库数额更新
        apply_amount = -1 * float(record_amount) if record_inout == 'out' else float(record_amount)
        cur.execute(""" SELECT money FROM e_money_position WHERE name_en = ?; """, (record_position,))
        money_before = float(cur.fetchone()[0])
        money_after = round(money_before + float(apply_amount), 2)
        cur.execute("""
            UPDATE e_money_position SET
            money = ? 
            WHERE name_en = ?
        """, (str(money_after), record_position))

    # 返回不同提示，便于前端判断
    if before_inout == 'transfer':
        return HttpResponse('资金记录 | 类型由 转移 -> 普通，信息修改成功 ！')
    else:
        return HttpResponse('资金记录 | 信息修改成功 ！')
