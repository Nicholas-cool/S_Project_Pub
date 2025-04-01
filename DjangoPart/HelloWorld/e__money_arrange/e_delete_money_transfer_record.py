from django.http import HttpResponse
import sqlite3


def e_delete_money_transfer_record(request):
    """ 删除 资金转移记录条目 """
    record_id = request.GET.get('record_id')

    # 创建数据库连接
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 获取原记录信息
    cur.execute("""SELECT position, inout, amount, fee FROM e_money_record WHERE id = ?;""", (record_id, ))
    before_position, before_inout, before_amount, before_fee = cur.fetchone()

    # money_position 数据库数额更新（原记录退回）
    before_position_from, before_position_to = before_position.split('&&')

    cur.execute(""" SELECT money FROM e_money_position WHERE name_en = ?; """, (before_position_from, ))
    money_before = float(cur.fetchone()[0])
    money_after = round(money_before + float(before_amount) + float(before_fee), 2)
    cur.execute("""
        UPDATE e_money_position SET money = ? WHERE NAME_EN = ?;
    """, (str(money_after), before_position_from))

    cur.execute(""" SELECT money FROM e_money_position WHERE name_en = ?; """, (before_position_to, ))
    money_before = float(cur.fetchone()[0])
    money_after = round(money_before - float(before_amount), 2)
    cur.execute("""
        UPDATE e_money_position SET money = ? WHERE NAME_EN = ?
    """, (str(money_after), before_position_to))

    # 删除记录信息
    cur.execute(""" DELETE FROM e_money_record WHERE id = ?;""", (record_id, ))
    conn.commit()

    # 关闭数据库连接
    cur.close()
    conn.close()

    return HttpResponse('资金转移记录 | 删除成功 ！')
