import unittest
import sqlite3
from tqdm import tqdm


class DBTestCase(unittest.TestCase):
    """ 数据库数据检查测试类 """

    def test_check_time_record(self):
        """ c_time_record 表检查 """
        # 创建数据库连接
        conn = sqlite3.connect('../../../data.db')
        cur = conn.cursor()

        # 检查 `c_time_record` 表中 `TASK_ID` 列均来自于 `c_task_form` 表
        cur.execute(" SELECT task_id FROM c_task_form; ")
        task_id_list = [_[0] for _ in cur.fetchall()]

        cur.execute(" SELECT TASK_ID FROM c_time_record; ")
        time_record_task_id_list = [_[0] for _ in cur.fetchall()]

        # 关闭数据库连接
        cur.close()
        conn.close()

        # 进行校验
        for _ in tqdm(time_record_task_id_list):
            self.assertIn(_, task_id_list)
