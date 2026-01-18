from django.http import JsonResponse
from ..z__common.z_db_get_cursor import get_cursor


def e_get_money_record(request):
    """ 获取 单个资金记录条目 """
    record_id = request.GET.get('record_id')

    with get_cursor() as cur:
        cur.execute(""" 
            SELECT id, name, type, amount, inout, position, description, date_str, fee, ledger, status, record_mode
            FROM e_money_record WHERE ID = '%s';
        """ % record_id)

        single_record = cur.fetchone()
        single_record_dic = {
            'id': single_record[0],
            'name': single_record[1],
            'type': single_record[2],
            'amount': single_record[3],
            'inout': single_record[4],
            'position': single_record[5],
            'description': single_record[6],
            'date': single_record[7],
            'fee': single_record[8],
            'ledger': single_record[9],
            'status': single_record[10],
            'mode': single_record[11] if single_record[11] else 'clean',
        }

    return JsonResponse(single_record_dic)
