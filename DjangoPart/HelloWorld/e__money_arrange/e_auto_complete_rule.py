from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
from ..z__common.z_db_get_cursor import get_cursor
import json
import time


class EAutoCompleteRule(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        """ 获取自动填充规则 """
        # 优先级重整
        with get_cursor() as cur:
            cur.execute(""" select rule_id from e_money_record_auto_complete order by priority; """)
            for idx, rule in enumerate(cur.fetchall()):
                cur.execute("""
                    update e_money_record_auto_complete set priority = ? where rule_id = ?;
                """, (idx + 1, rule[0]))

        # 获取所有自动填充规则
        with get_cursor() as cur:
            # 获取 position 的对应中文信息
            cur.execute(""" select name_en, name from e_money_position; """)
            position_dic = {_[0]: _[1] for _ in cur.fetchall()}

            # 自动填充规则列表（带顺序信息）
            cur.execute(""" 
                select rule_id, pattern, inout, type, position, amount, priority 
                from e_money_record_auto_complete order by priority;
            """)

            auto_complete_rule_lst = [
                [_[idx] for idx in range(7)] + [position_dic.get(_[4], '')] for _ in cur.fetchall()
            ]

        return JsonResponse(auto_complete_rule_lst, safe=False)

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        """ 添加自动填充规则 """
        rule_name = request.POST.get('rule_name')
        rule_position = request.POST.get('rule_position')
        rule_inout = request.POST.get('rule_inout')
        rule_category = request.POST.get('rule_category')
        rule_amount = request.POST.get('rule_amount')
        rule_priority = request.POST.get('rule_priority')

        with get_cursor() as cur:
            cur.execute(""" 
                insert into e_money_record_auto_complete (rule_id, pattern, position, inout, type, amount, priority)
                values (?, ?, ?, ?, ?, ?, ?);
            """, (round(time.time()), rule_name, rule_position, rule_inout, rule_category, rule_amount, rule_priority)
            )

        return HttpResponse('自动填充规则 | 添加成功！')

    # noinspection PyMethodMayBeStatic
    def put(self, request):
        """ 更新自动填充规则 """
        data = json.loads(request.body)
        rule_id = data.get('rule_id')
        rule_name = data.get('rule_name')
        rule_position = data.get('rule_position')
        rule_inout = data.get('rule_inout')
        rule_category = data.get('rule_category')
        rule_amount = data.get('rule_amount')
        rule_priority = data.get('rule_priority')

        if not rule_priority:
            with get_cursor() as cur:
                cur.execute(""" 
                    update e_money_record_auto_complete 
                    set pattern = ?, position = ?, inout = ?, type = ?, amount = ?
                    where rule_id = ?;
                """, (rule_name, rule_position, rule_inout, rule_category, rule_amount, rule_id))
        else:
            with get_cursor() as cur:
                cur.execute(""" 
                    update e_money_record_auto_complete 
                    set priority = ? where rule_id = ?;
                """, (rule_priority, rule_id))

        return HttpResponse('自动填充规则 | 更新成功！')

    # noinspection PyMethodMayBeStatic
    def delete(self, request):
        """ 删除自动填充规则 """
        data = json.loads(request.body)
        rule_id = data.get('rule_id')

        with get_cursor() as cur:
            cur.execute(""" delete from e_money_record_auto_complete where rule_id = ?; """, (rule_id, ))

        return HttpResponse('自动填充规则 | 删除成功！')
