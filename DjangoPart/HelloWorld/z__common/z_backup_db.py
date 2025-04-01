from django.shortcuts import HttpResponse
import os
import shutil
import datetime
import time


class DBBackup(object):

    def copy_file(self, source, target, date_info):
        # adding exception handling
        try:
            shutil.copy(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)

        # rename the file
        old_name = target + '\\' + os.path.basename(source)
        new_name = target + '\\' + os.path.splitext(os.path.basename(source))[0] + date_info + \
                   os.path.splitext(os.path.basename(source))[1]
        os.rename(old_name, new_name)

    def db_restore(self):
        source_location = 'data.db'
        target_location = 'data_store'
        date_info = str(datetime.date.today()) + str(time.strftime("-%H-%M-%S"))
        self.copy_file(source_location, target_location, date_info)


def y_backup_db(request):
    """ 实现数据库文件自动备份功能 """
    db_backup = DBBackup()
    db_backup.db_restore()

    return HttpResponse('数据库备份成功！')
