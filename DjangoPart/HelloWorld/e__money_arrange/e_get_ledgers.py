from django.http import JsonResponse
import sqlite3


def cal_ledger_statistics(ledger_id, cur):
    cur.execute(""" 
        select AMOUNT, INOUT, DATE_STR, FEE from e_money_record
        where LEDGER = '%s';
    """ % ledger_id)

    start_date, end_date = '', ''
    income_amount, outcome_amount = 0, 0
    for row in cur.fetchall():
        start_date = row[2] if not start_date or row[2] < start_date else start_date
        end_date = row[2] if not end_date or row[2] > end_date else end_date

        if row[1] == 'out':
            outcome_amount += float(row[0])
        elif row[1] == 'in':
            income_amount += float(row[0])
        elif row[1] == 'transfer':
            outcome_amount += float(row[3])
        else:
            raise ValueError

    return start_date, end_date, round(income_amount, 2), round(outcome_amount, 2)


def e_get_ledgers(request):
    """ 从数据库中获取账本列表信息 """
    ledger_id = request.GET.get('ledger_id', '')

    # 创建数据库连接
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    money_ledger_dic = {}
    if ledger_id:  # 如果存在 ledger_id 参数，则获取单条记录
        cur.execute(""" 
            select ledger_id, name, desc, category from e_money_ledger where ledger_id = ?; 
        """, (ledger_id, ))
    else:
        cur.execute("""  select ledger_id, name, desc, category from e_money_ledger; """)

    for line in cur.fetchall():
        # 计算每个账本的时间范围和总计收支
        statistics_info = cal_ledger_statistics(line[0], cur)

        # 账本中记录的时间范围计算，并按结束时间排序

        money_ledger_dic[line[0]] = {
            'name': line[1],
            'desc': line[2],
            'category': line[3],
            'start_date': statistics_info[0],
            'end_date': statistics_info[1],
            'income_amount': statistics_info[2],
            'outcome_amount': statistics_info[3],
        }

    # 关闭数据库连接
    cur.close()
    conn.close()

    return JsonResponse(money_ledger_dic)
