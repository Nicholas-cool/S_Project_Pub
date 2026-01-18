from django.http import HttpResponse
from .e_modify_money_record import recover_inout_impact, recover_transfer_impact
from ..z__common.z_db_get_cursor import get_cursor


def e_delete_money_record(request):
    """ 删除资金记录（含资金转移记录） """
    record_id = request.GET.get('record_id')

    # 获取原记录信息
    with get_cursor() as cur:
        cur.execute(""" select inout from e_money_record where id = ?; """, (record_id, ))
        record_inout = cur.fetchone()[0]

    if record_inout == 'transfer':
        recover_transfer_impact(record_id)
    elif record_inout in ('in', 'out'):
        recover_inout_impact(record_id)
    else:
        return HttpResponse('资金记录 | 删除失败（数据库资金记录类型错误） ！')

    # 删除记录信息
    with get_cursor() as cur:
        cur.execute(""" DELETE FROM e_money_record WHERE id = ?; """, (record_id, ))

    if record_inout == 'transfer':
        return HttpResponse('资金转移记录 | 删除成功 ！')
    else:
        return HttpResponse('资金记录 | 删除成功 ！')
