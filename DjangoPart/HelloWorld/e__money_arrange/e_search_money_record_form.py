from django.http import JsonResponse
import sqlite3
import datetime
import copy


# 确定行结果是否符合 搜索的文本
def correspond(line, search_text, search_start_date, search_end_date,
               search_inout, search_category, search_position, search_ledger_id):

    # 搜索语句的验证
    if search_text.lower() not in line[1].lower():
        return False

    # 收支类型的验证
    if search_inout != 'all':
        if search_inout != line[4]:
            return False

    # 分类的验证
    if search_category != 'all':
        if search_category != line[2]:
            return False

    # 来源的验证
    if search_position != 'all':
        if (search_position != line[5] and (not str(line[5]).startswith((search_position + '&&')))
                and (not str(line[5]).endswith('&&' + search_position))):
            return False

    # 时间范围的验证
    record_date = datetime.datetime.strptime(line[7], '%Y-%m-%d')

    if search_start_date:
        start_date = datetime.datetime.strptime(search_start_date, '%Y-%m-%d')
        if record_date < start_date:
            return False

    if search_end_date:
        end_date = datetime.datetime.strptime(search_end_date, '%Y-%m-%d')
        if record_date > end_date:
            return False

    # 账本的验证
    if search_ledger_id and search_ledger_id != line[9]:
        return False

    return True


def e_search_money_record_form(request):
    """ 获取 money_record 的搜索结果，并按照 layUI 表格 需要的形式返回 """

    # 得到当前页码 page，每页的数据量 limit
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))

    search_text = request.GET.get('search_text', '')
    search_start_date = request.GET.get('search_start_date', '')
    search_end_date = request.GET.get('search_end_date', '')
    search_inout = request.GET.get('search_inout', 'all')
    search_category = request.GET.get('search_category', 'all')
    search_position = request.GET.get('search_position', 'all')
    search_order = request.GET.get('search_order', 'default')
    search_ledger_id = request.GET.get('search_ledger_id', '')

    search_money_record_ids = eval(request.GET.get('record_ids', '[]'))   # 指定获取的记录 id

    # 创建数据库连接
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 获取 money_position 对应中文信息
    money_position_map = {}
    cur.execute(""" select NAME_EN, NAME from e_money_position; """)
    for line in cur.fetchall():
        money_position_map[line[0]] = line[1]

    # 获取账本对应的名字信息
    ledger_map = {}
    cur.execute(""" select ledger_id, NAME from e_money_ledger; """)
    for line in cur.fetchall():
        ledger_map[line[0]] = line[1]

    # 查询记录的信息，返回列表数据
    cur.execute(""" 
        select ID, NAME, TYPE, AMOUNT, INOUT, POSITION, DESCRIPTION, DATE_STR, STATUS, LEDGER
        FROM e_money_record ORDER BY ID DESC;
    """)
    all_record = []
    all_record_query = cur.fetchall()

    # 查询出来的数据，通过匹配筛选并加入结果集
    for line in all_record_query:
        # 如果符合搜索条件，则加入结果集
        if(correspond(copy.deepcopy(line), search_text, search_start_date, search_end_date,
                      search_inout, search_category, search_position, search_ledger_id)):

            if '&&' in line[5]:
                position_str = '&&'.join([money_position_map[_] for _ in line[5].split('&&')])
            else:
                position_str = money_position_map[line[5]]

            record_dic = {
                'id': line[0],
                'name': line[1],
                'type': line[2],
                'amount': line[3],
                'inout': line[4],
                'position': position_str,
                'description': line[6],
                'date': line[7],
                'status': line[8],
                'ledger_name': '' if not line[9] else ledger_map[line[9]],
            }
            all_record.append(record_dic)

    # 基于 ids 再次筛选
    if search_money_record_ids:
        all_record = [_ for _ in all_record if _['id'] in search_money_record_ids]

    # 重新排序
    if search_order == 'default':
        all_record.sort(key=lambda x: x['id'], reverse=True)
    elif search_order == 'date_desc':
        all_record.sort(key=lambda x: x['date'], reverse=True)
    elif search_order == 'amount_desc':
        all_record.sort(key=lambda x: float(x['amount']), reverse=True)

    # 分页数据返回
    count = len(all_record)   # 记录总数
    all_record = all_record[(page - 1) * limit: page * limit]

    # 添加索引（从 0 开始，和 layUI 表格本身的索引保持一致）
    row_idx = 0
    for ele_dic in all_record:
        ele_dic['index'] = row_idx
        row_idx += 1

    # 关闭数据库连接
    cur.close()
    conn.close()

    # 按照 LayUI 表格所需形式准备数据
    response_result = {
      "code": 0,
      "msg": "",
      "count": count,
      "data": all_record
    }
    return JsonResponse(response_result)
