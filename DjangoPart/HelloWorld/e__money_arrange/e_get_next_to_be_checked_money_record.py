from django.http import JsonResponse
from ..z__common.z_db_get_cursor import get_cursor


def e_get_next_to_be_checked_money_record(request):
    """ 获取 ID 更大且 status 为 to_be_checked 的首条资金记录；
        若不存在则环回返回最小 ID 的待确认记录
    """
    current_id = request.GET.get('current_id', 0)

    with get_cursor() as cur:
        # 先查找 ID 更大的待确认记录
        cur.execute("""
            SELECT id, inout FROM e_money_record
            WHERE status = 'to_be_checked' AND id > ?
            ORDER BY id ASC
            LIMIT 1;
            """, (current_id,)
        )
        row = cur.fetchone()

        # 若没有更大 ID 的记录，则环回到最小 ID 的待确认记录
        if not row:
            cur.execute("""
                SELECT id, inout FROM e_money_record
                WHERE status = 'to_be_checked'
                ORDER BY id ASC
                LIMIT 1;
                """
            )
            row = cur.fetchone()

    if row:
        return JsonResponse({'id': row[0], 'inout': row[1]})
    else:
        return JsonResponse({})
