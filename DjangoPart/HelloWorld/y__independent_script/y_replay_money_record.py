"""
    从最近一次归档记录重放资金记录（用于修正错误的 money_position 数据）
"""

import unittest
import sqlite3
from tqdm import tqdm


class ReplayMoneyRecord(unittest.TestCase):
    """ 资金记录重放测试类 """

    def test_reply_money_record(self):
        """ 重放资金记录 """

        # TODO: 首先判断数据库文件是否存在，如果不存在则直接退出（防止空的 data.db 被创建出来）

        # 创建数据库连接
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        # 获取最近一次归档的数据
        cur.execute(""" select archive_time from e_money_archive order by archive_time desc limit 1; """)
        last_archive_time = cur.fetchone()[0]

        cur.execute(""" 
            select position, money from e_money_archive where archive_time = ?; 
        """, (last_archive_time,))
        last_archive_data = cur.fetchall()
        last_archive_data_dic = {_[0]: _[1] for _ in last_archive_data}

        # 更新 money_position 表中的数据为归档时的数据（不允许有被删除的 money position）
        cur.execute("""
            select name_en, money from e_money_position;
        """)
        now_data = cur.fetchone()
        now_data_dic = {_[0]: _[1] for _ in now_data}

        for position in now_data_dic:
            if position not in last_archive_data_dic:
                last_archive_data_dic[position] = 0

        for position, money in last_archive_data_dic.items():
            cur.execute("""
                update e_money_position set money = ? where name_en = ?; 
            """, (money, position))

        # 重放归档时间后的资金记录（这里只能精确到天，因此可能有些许不准确）
        cur.execute("""
            select amount, inout, position, fee from e_money_record where date_str > ?;
        """, (last_archive_time,))

        records = cur.fetchall()
        print(f'需要重放的资金记录条目数量: {len(records)}')
        for amount, inout, position, fee in tqdm(records):
            if inout in ['in', 'out']:
                cur.execute(""" select money from e_money_position where name_en = ?; """, (position,))
                money_before, money_after = float(cur.fetchone()[0]), None
                if inout == 'in':
                    money_after = round(money_before + float(amount), 2)
                elif inout == 'out':
                    money_after = round(money_before - float(amount), 2)
                cur.execute(""" 
                    update e_money_position set money = ? where name_en = ?; 
                """, (str(money_after), position))

            elif inout == 'transfer':
                cur.execute(""" select money from e_money_position where name_en = ?; """, (position.split('&&')[0],))
                money_before = float(cur.fetchone()[0])
                money_after = round(money_before - float(amount) - float(fee), 2)
                cur.execute(""" update e_money_position set money = ? where name_en = ?; """,
                            (str(money_after), position.split('&&')[0]))

                cur.execute(""" select money from e_money_position where name_en = ?; """, (position.split('&&')[1],))
                money_before = float(cur.fetchone()[0])
                money_after = round(money_before + float(amount), 2)
                cur.execute(""" update e_money_position set money = ? where name_en = ?; """,
                            (str(money_after), position.split('&&')[1]))

            else:
                raise ValueError(f'未知的资金流向类型: {inout}')
        conn.commit()

        # 关闭数据库连接
        cur.close()
        conn.close()
