"""
    垃圾清理，和相关数据库无关联的文件（相关数据库中数据删除导致）
"""

import unittest
import sqlite3
import os
import shutil


class GarbageClean(unittest.TestCase):
    """ 垃圾清理测试类 """

    def test_clearn_human_attachment(self):
        """ 清理 human_attachment 文件夹中未被关联的文件 """

        # 创建数据库连接
        conn = sqlite3.connect('../../../data.db')
        cur = conn.cursor()

        cur.execute(""" select FILE_PATH, THUMBNAIL from m_human_attachment; """)
        cur_result = cur.fetchall()
        file_path_list = [_[0] for _ in cur_result]
        thumbnail_list = [_[1] for _ in cur_result if _[1]]
        # print(file_path_list)

        # 关闭数据库连接
        cur.close()
        conn.close()

        # 遍历 human_attachment 文件夹，将未被关联的文件移动到回收站文件夹
        folder_path = '../../media/human_attachment/'
        count_link, count_link_thumbnail, count_unlink = 0, 0, 0
        unlinked_file_list = []
        for file_path, dir_names, file_names in os.walk(folder_path):
            for file_name in file_names:
                match_path = os.path.join(file_path, file_name).replace('../..', '').replace('\\', '/')
                if match_path in file_path_list:
                    count_link += 1
                elif match_path in thumbnail_list:
                    count_link_thumbnail += 1
                else:
                    # print(match_path)
                    unlinked_file_list.append(match_path)
                    count_unlink += 1

        # 检验数据库中的文件数量和实际文件数量是否一致
        print(f'数据库中文件数量：{len(file_path_list) + len(thumbnail_list)} '
              f'（其中 具体文件 {len(file_path_list)} 项，缩略图 {len(thumbnail_list)} 项）\n'
              f'实际关联文件数量：{count_link + count_link_thumbnail} '
              f'（其中 具体文件 {count_link} 项，缩略图 {count_link_thumbnail} 项）\n'
              f'未关联文件数量：{count_unlink}\n')
        self.assertEqual(count_link, len(file_path_list))
        self.assertEqual(count_link_thumbnail, len(thumbnail_list))

        # 移动未关联文件到回收站
        for relative_path in unlinked_file_list:
            src_str = f'../..{relative_path}'
            dest_str = f'../../media/recycle_bin/{relative_path.replace("/media/", "")}'
            print(f'{src_str} \n==>\n{dest_str} \n')

            # 创建目标文件夹
            dest_folder = os.path.dirname(dest_str)
            os.makedirs(dest_folder, exist_ok=True)

            # 移动文件
            shutil.move(src_str, dest_str)
