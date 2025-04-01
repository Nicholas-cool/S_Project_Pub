from django.http import JsonResponse
import sqlite3


def e_get_money_positions(request):
    """ 从数据库中获取 money_positions 详细信息 """

    # 创建数据库连接
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # 获取 money_position 对应中文信息
    money_position_dic = {}
    cur.execute(""" select name_en, name, money, type, addition_info, hidden from e_money_position; """)
    for line in cur.fetchall():
        money_position_dic[line[0]] = {
            'name': line[1],
            'money': line[2],
            'type': line[3],
            'addition_info': line[4],
            'hidden': line[5],
        }

    # 关闭数据库连接
    cur.close()
    conn.close()

    return JsonResponse(money_position_dic)
